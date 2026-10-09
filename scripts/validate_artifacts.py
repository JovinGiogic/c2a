#!/usr/bin/env python3
"""Check C2A artifact structure and correspondence; semantic/visual review stays human/Agent work."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
from urllib.parse import unquote, urlsplit

from find_references import KINDS, read_catalog


class ValidationError(ValueError):
    pass


def require(condition: object, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def obj(value: object, label: str) -> dict:
    require(isinstance(value, dict), f"{label}: expected an object")
    return value


def seq(value: object, label: str) -> list:
    require(isinstance(value, list), f"{label}: expected a list")
    return value


def text(value: object, label: str) -> str:
    require(isinstance(value, str) and value.strip(), f"{label}: expected nonempty text")
    return value


def strings(value: object, label: str) -> list[str]:
    result = seq(value, label)
    for item in result:
        text(item, label)
    return result


def records(value: object, label: str) -> dict[str, dict]:
    result = {}
    for row in seq(value, label):
        row = obj(row, label)
        identifier = text(row.get("id"), f"{label}.id")
        require(re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", identifier), f"{label}: invalid ID {identifier}")
        require(identifier not in result, f"{label}: duplicate ID {identifier}")
        result[identifier] = row
    return result


def relative_path(root: Path, value: object, label: str, exists: bool = True) -> Path:
    name = text(value, label)
    p = PurePosixPath(name)
    require(not p.is_absolute() and ".." not in p.parts and "\\" not in name
            and not re.match(r"^[A-Za-z]:", name) and "\x00" not in name,
            f"{label}: expected a contained relative path")
    resolved = (root / name).resolve()
    require(resolved.is_relative_to(root.resolve()), f"{label}: path escapes its root")
    if exists:
        require(resolved.is_file(), f"{label}: missing file {name}")
    return resolved


def read_json(path: Path) -> dict:
    try:
        return obj(json.loads(path.read_text(encoding="utf-8")), str(path))
    except (OSError, ValueError) as error:
        raise ValidationError(f"Cannot read JSON {path}: {error}") from error


def markdown_links(path: Path, root: Path) -> set[Path]:
    content = path.read_text(encoding="utf-8")
    resolved_links = set()
    # Templates describe their future links in prose; delivered guides use actual links.
    for raw in re.findall(r"\[[^\]\n]*\]\(([^)\n]+)\)", content):
        target = raw[1:raw.index(">")] if raw.startswith("<") and ">" in raw else raw.split()[0]
        parsed = urlsplit(target)
        if parsed.scheme or not parsed.path:
            continue
        local = (path.parent / unquote(parsed.path)).resolve()
        require(local.is_relative_to(root.resolve()), f"{path.name}: link escapes its root: {target}")
        require(local.exists(), f"{path.name}: broken link: {target}")
        resolved_links.add(local)
    return resolved_links


def check_evidence(value: object, label: str, source_root: Path | None) -> None:
    entries = seq(value, label)
    require(entries, f"{label}: source evidence is required")
    for entry in entries:
        entry = obj(entry, label)
        path = relative_path(source_root or Path.cwd(), entry.get("path"), label,
                             exists=source_root is not None)
        text(entry.get("symbol"), f"{label}.symbol")
        text(entry.get("supports"), f"{label}.supports")
        if "lines" in entry:
            bounds = seq(entry["lines"], f"{label}.lines")
            require(len(bounds) == 2 and all(type(n) is int for n in bounds)
                    and 1 <= bounds[0] <= bounds[1], f"{label}: invalid line range")
            if source_root:
                count = len(path.read_text(encoding="utf-8").splitlines())
                require(bounds[1] <= count, f"{label}: line range exceeds source file")


def validate_spec(spec: dict, source_root: Path | None = None) -> None:
    require(spec.get("schema_version") == "1.0", "spec: unsupported schema_version")
    text(spec.get("analysis_id"), "spec.analysis_id")
    text(spec.get("summary"), "spec.summary")
    source = obj(spec.get("source"), "spec.source")
    text(source.get("label"), "source.label")
    require(source.get("revision") is None or isinstance(source["revision"], str), "source.revision: expected text or null")
    text(source.get("working_tree"), "source.working_tree")
    strings(source.get("scope"), "source.scope")
    strings(source.get("excluded"), "source.excluded")
    modules = records(spec.get("modules"), "modules")
    require(modules, "spec: at least one supported module is required")
    edges = records(spec.get("relationships"), "relationships")
    groups = records(spec.get("groups"), "groups")
    flows = records(spec.get("flows"), "flows")
    uncertainties = records(spec.get("uncertainties"), "uncertainties")
    all_ids = list(modules) + list(edges) + list(groups) + list(flows) + list(uncertainties)
    require(len(set(all_ids)) == len(all_ids), "spec: IDs must be unique across entity types")
    for identifier, module in modules.items():
        label = text(module.get("label"), f"{identifier}.label")
        require(not re.search(r"[\u3400-\u9fff]", label), f"{identifier}: display label must be English")
        text(module.get("responsibility"), f"{identifier}.responsibility")
        require(module.get("kind") in {"component", "external", "store", "artifact", "actor"}, f"{identifier}: invalid module kind")
        check_evidence(module.get("evidence"), identifier, source_root)
    edge_kinds = {"call", "data", "control", "event", "state_update", "training", "dependency", "ownership", "deployment"}
    for identifier, edge in edges.items():
        require(edge.get("source") in modules and edge.get("target") in modules, f"{identifier}: dangling edge endpoint")
        require(edge.get("kind") in edge_kinds, f"{identifier}: invalid relationship kind")
        text(edge.get("meaning"), f"{identifier}.meaning")
        require(edge.get("certainty") in {"observed", "inferred"}, f"{identifier}: invalid certainty")
        if edge["certainty"] == "inferred":
            text(edge.get("derivation"), f"{identifier}.derivation")
        check_evidence(edge.get("evidence"), identifier, source_root)
    for identifier, group in groups.items():
        text(group.get("label"), f"{identifier}.label")
        text(group.get("meaning"), f"{identifier}.meaning")
        members = strings(group.get("members"), f"{identifier}.members")
        require(members and all(m in modules for m in members), f"{identifier}: invalid group member")
        require(len(set(members)) == len(members), f"{identifier}: repeated group member")
    for identifier, flow in flows.items():
        text(flow.get("label"), f"{identifier}.label")
        text(flow.get("phase"), f"{identifier}.phase")
        nodes = strings(flow.get("module_ids"), f"{identifier}.module_ids")
        relations = strings(flow.get("relationship_ids"), f"{identifier}.relationship_ids")
        require(nodes and all(n in modules for n in nodes), f"{identifier}: unknown flow module")
        require(all(e in edges for e in relations), f"{identifier}: unknown flow relation")
        require(all(edges[e]["source"] in nodes and edges[e]["target"] in nodes for e in relations), f"{identifier}: flow omits an endpoint")
    for term in seq(spec.get("terms"), "terms"):
        term = obj(term, "term")
        for field in ("source_term", "display_label", "meaning"):
            text(term.get(field), f"term.{field}")
    for identifier, uncertainty in uncertainties.items():
        for field in ("question", "impact", "resolution"):
            text(uncertainty.get(field), f"{identifier}.{field}")
        affected = strings(uncertainty.get("affected_ids"), f"{identifier}.affected_ids")
        require(all(item in all_ids for item in affected), f"{identifier}: unknown affected ID")


def check_prompt(path: Path, reference_count: int) -> None:
    content = path.read_text(encoding="utf-8")
    require(content.strip(), f"{path.name}: empty prompt")
    require(re.search(r"\ball visible text\b[^.\n]*\bEnglish\b", content, re.I), "prompt: explicitly require English for all visible text")
    require(re.search(r"Comic Sans MS[^.\n]*all visible text|all visible text[^.\n]*Comic Sans MS", content, re.I), "prompt: require Comic Sans MS for all visible text")
    require(not re.search(r"[\u3400-\u9fff]", content), "prompt: contains non-English CJK text")
    require(not re.search(r"\{\{.*?\}\}|\[TODO\b", content, re.S), "prompt: unfilled template placeholder")
    require(not re.search(r"architecture-spec\.json|code-analysis\.md", content, re.I), "prompt: depends on an internal analysis artifact")
    mentioned = {int(n) for n in re.findall(r"\bReference Image\s+(\d+)\b", content, re.I)}
    require(mentioned == set(range(1, reference_count + 1)), "prompt: reference numbers do not match attachments")


def check_image(path: Path) -> None:
    require(path.stat().st_size > 0, f"{path.name}: empty image")
    if path.suffix.lower() == ".png":
        with path.open("rb") as stream:
            header = stream.read(24)
        require(len(header) == 24 and header[:8] == b"\x89PNG\r\n\x1a\n"
                and header[12:16] == b"IHDR"
                and int.from_bytes(header[16:20], "big") > 0
                and int.from_bytes(header[20:24], "big") > 0, f"{path.name}: invalid PNG header")


def check_references(root: Path, value: object, prefix: str) -> list[dict]:
    refs = seq(value, "reference_images")
    for number, ref in enumerate(refs, 1):
        ref = obj(ref, "reference image")
        require(ref.get("id") == f"R{number}", "references: use consecutive R1, R2, ... IDs in attachment order")
        path = relative_path(root, ref.get("path"), "reference path")
        require(ref["path"].startswith(prefix + "references/"), "reference: must be copied inside its package")
        require(path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif", ".avif"}, "reference: use an uploadable image preview")
        check_image(path)
        require(ref.get("origin") in {"library", "user", "returned_image"}, "reference: invalid origin")
        require(strings(ref.get("borrow"), "reference.borrow"), "reference: specify what to borrow")
        require(strings(ref.get("avoid"), "reference.avoid"), "reference: specify borrowing limits")
        if ref["origin"] == "library":
            text(ref.get("asset_id"), "reference.asset_id")
        if ref["origin"] == "returned_image":
            for field in ("source_candidate_id", "source_version_id", "source_image_id"):
                text(ref.get(field), f"reference.{field}")
    return refs


def check_guide(root: Path, guide: Path, prompt: Path, refs: list[dict]) -> None:
    links = markdown_links(guide, root)
    require(prompt.resolve() in links, "reference guide: missing link to the complete prompt")
    for ref in refs:
        require((root / ref["path"]).resolve() in links, f"reference guide: missing link for {ref['id']}")


def validate_run(root: Path, source_root: Path | None = None) -> dict:
    root = root.resolve()
    manifest = read_json(root / "manifest.json")
    require(manifest.get("schema_version") == "1.0", "manifest: unsupported schema_version")
    text(manifest.get("project_id"), "manifest.project_id")
    require(manifest.get("active_stage") in {f"S{n}" for n in range(6)}, "manifest: invalid active_stage")
    analyses = records(manifest.get("analyses"), "analyses")
    current = manifest.get("current_analysis_id")
    require(current is None or current in analyses, "manifest: unknown current_analysis_id")
    for identifier, analysis in analyses.items():
        for field in ("report", "spec"):
            relative_path(root, analysis.get(field), f"{identifier}.{field}")
            require(analysis[field].startswith(f"analysis/{identifier}/"), f"{identifier}: analysis path/ID mismatch")
        text((root / analysis["report"]).read_text(encoding="utf-8"), f"{identifier}: analysis report")
        spec = read_json(root / analysis["spec"])
        require(spec.get("analysis_id") == identifier, f"{identifier}: specification analysis_id mismatch")
        validate_spec(spec, source_root if identifier == current else None)
    if manifest.get("candidate_plan") is not None:
        plan = relative_path(root, manifest["candidate_plan"], "candidate_plan")
        text(plan.read_text(encoding="utf-8"), "candidate plan")
    candidates = records(manifest.get("candidates"), "candidates")
    if candidates:
        require(current is not None, "candidates: current analysis is required")
        require(manifest.get("candidate_plan") is not None, "candidates: candidate_plan is required")
    versions = {}
    pending_references = []
    image_count = 0
    allowed_statuses = {"draft", "ready", "awaiting_images", "images_received", "reviewed", "superseded"}
    for cid, candidate in candidates.items():
        for vid, version in records(candidate.get("versions"), f"{cid}.versions").items():
            key = (cid, vid)
            versions[key] = version
            prefix = f"candidates/{cid}/{vid}/"
            require(version.get("analysis_id") in analyses, f"{cid}/{vid}: unknown analysis_id")
            status = version.get("status")
            require(status in allowed_statuses, f"{cid}/{vid}: invalid status")
            text(version.get("change_note"), f"{cid}/{vid}.change_note")
            paths = {}
            for field in ("prompt", "reference_guide"):
                if version.get(field) is None:
                    require(status == "draft", f"{cid}/{vid}: {field} is required")
                else:
                    paths[field] = relative_path(root, version[field], f"{cid}/{vid}.{field}")
                    require(version[field].startswith(prefix), f"{cid}/{vid}: candidate/version path mismatch")
            refs = check_references(root, version.get("reference_images"), prefix)
            pending_references.extend((key, ref) for ref in refs if ref["origin"] == "returned_image")
            if status != "draft":
                check_prompt(paths["prompt"], len(refs))
                check_guide(root, paths["reference_guide"], paths["prompt"], refs)
            images = records(version.get("returned_images"), f"{cid}/{vid}.returned_images")
            image_count += len(images)
            for image in images.values():
                path = relative_path(root, image.get("path"), "returned image")
                require(image["path"].startswith(f"returned-images/{cid}/{vid}/"), "returned image: candidate/version path mismatch")
                require(image.get("origin") == "human", "returned image: origin must be human")
                check_image(path)
            covered = set()
            for review in seq(version.get("reviews"), f"{cid}/{vid}.reviews"):
                review = obj(review, "review")
                report = relative_path(root, review.get("path"), "review.path")
                text(report.read_text(encoding="utf-8"), "review report")
                require(review.get("basis") in {"direct", "human_observations"}, "review: disclose direct or human_observations basis")
                image_ids = strings(review.get("image_ids"), "review.image_ids")
                require(image_ids and all(i in images for i in image_ids), "review: unknown image or wrong candidate/version")
                covered.update(image_ids)
            if status in {"images_received", "reviewed"}:
                require(images, f"{cid}/{vid}: cannot claim image receipt/review without images")
            if status == "reviewed":
                require(covered == set(images), f"{cid}/{vid}: review does not cover all returned images")
            if images:
                require(status != "draft", f"{cid}/{vid}: returned images require a complete prompt version")
    for key, ref in pending_references:
        source_key = (ref["source_candidate_id"], ref["source_version_id"])
        require(source_key in versions and source_key != key, "reference: returned image must come from another existing version")
        source_images = records(versions[source_key]["returned_images"], "reference source images")
        require(ref["source_image_id"] in source_images, "reference: source_image_id does not exist")
    final = manifest.get("final")
    if final is not None:
        final = obj(final, "final")
        key = (final.get("candidate_id"), final.get("version_id"))
        require(key in versions, "final: selected candidate/version does not exist")
        chosen = versions[key]
        require(chosen["status"] != "draft", "final: cannot select a draft")
        require(final.get("analysis_id") == chosen["analysis_id"] == current, "final: recheck the selected version against the current analysis")
        require(final.get("selection_basis") in {"human_choice", "requested_prompt_only"}, "final: record selection basis")
        prompt = relative_path(root, final.get("prompt"), "final.prompt")
        guide = relative_path(root, final.get("reference_guide"), "final.reference_guide")
        require(final["prompt"] == "final/architecture-prompt.md", "final: use final/architecture-prompt.md")
        require(final["reference_guide"] == "final/reference-guide.md", "final: use final/reference-guide.md")
        refs = check_references(root, final.get("reference_images"), "final/")
        require(prompt.read_bytes() == (root / chosen["prompt"]).read_bytes(), "final: prompt differs from selected version; create a new version first")
        source_refs = chosen["reference_images"]
        require(len(refs) == len(source_refs), "final: attachment set differs from selected version")
        for ref, source_ref in zip(refs, source_refs):
            require({k: v for k, v in ref.items() if k != "path"} == {k: v for k, v in source_ref.items() if k != "path"}, "final: reference metadata differs from selected version")
            require(hashlib.sha256((root / ref["path"]).read_bytes()).digest()
                    == hashlib.sha256((root / source_ref["path"]).read_bytes()).digest(), "final: attachment content differs from selected version")
        check_prompt(prompt, len(refs))
        check_guide(root, guide, prompt, refs)
    if manifest["active_stage"] == "S5":
        require(final is not None, "S5: final package is missing")
    return {"analyses": len(analyses), "candidates": len(candidates), "versions": len(versions),
            "returned_images": image_count, "final_package": final is not None}


def validate_package(root: Path) -> dict:
    root = root.resolve()
    skill = (root / "SKILL.md").read_text(encoding="utf-8")
    require(re.search(r"^name: c2a$", skill, re.M), "SKILL.md: expected skill name c2a")
    metadata = read_json(root / "metadata.json")
    require(metadata.get("name") == "c2a" and metadata.get("entrypoint") == "SKILL.md", "metadata: entrypoint/name mismatch")
    for path in (root / "templates").glob("*.json"):
        read_json(path)
    documents = [root / "SKILL.md", root / "README.md"]
    for directory in ("references", "templates", "assets"):
        documents.extend((root / directory).rglob("*.md"))
    for path in documents:
        markdown_links(path, root)
    catalog = read_catalog(root / "assets/reference-index.jsonl")
    require(catalog, "reference catalog is empty")
    ids = set()
    checked_images = set()
    for entry in catalog:
        identifier = text(entry.get("asset_id"), "asset_id")
        require(identifier not in ids, f"catalog: duplicate asset_id {identifier}")
        ids.add(identifier)
        text(entry.get("title"), f"{identifier}.title")
        require(entry.get("kind") in KINDS, f"{identifier}: unknown asset kind")
        strings(entry.get("tags"), f"{identifier}.tags")
        require(strings(entry.get("borrow"), f"{identifier}.borrow"), f"{identifier}: missing borrowing scope")
        require(strings(entry.get("avoid"), f"{identifier}.avoid"), f"{identifier}: missing borrowing limits")
        obj(entry.get("provenance"), f"{identifier}.provenance")
        relative_path(root, entry.get("source_path"), f"{identifier}.source_path")
        preview = relative_path(root, entry.get("preview_path"), f"{identifier}.preview_path")
        require(preview.suffix.lower() == ".png", f"{identifier}: provide a portable PNG preview")
        if preview not in checked_images:
            check_image(preview)
            checked_images.add(preview)
        if "source_page" in entry:
            require(type(entry["source_page"]) is int and entry["source_page"] >= 1, f"{identifier}: invalid source page")
    return {"markdown_documents": len(documents), "reference_entries": len(catalog), "reference_previews": len(checked_images)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--package", type=Path, help="Validate an installed C2A package")
    mode.add_argument("--run", type=Path, help="Validate a C2A run directory")
    parser.add_argument("--source-root", type=Path, help="Optional current source checkout for evidence path/line checks")
    args = parser.parse_args()
    if args.source_root and not args.run:
        parser.error("--source-root requires --run")
    try:
        result = validate_package(args.package) if args.package else validate_run(args.run, args.source_root)
    except (OSError, ValueError, TypeError, KeyError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print("PASS: structural checks " + json.dumps(result, ensure_ascii=False))
    print("Code fidelity, language quality, and actual image/font appearance require separate review.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
