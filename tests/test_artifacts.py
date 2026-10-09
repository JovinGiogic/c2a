"""Behavior tests for portable handoffs. Tiny images simulate human-supplied files."""

from __future__ import annotations

import copy
import json
from pathlib import Path
import shutil
import struct
import sys
import tempfile
import unittest
import zlib

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from validate_artifacts import ValidationError, validate_run, validate_spec  # noqa: E402


def tiny_png() -> bytes:
    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xffffffff)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 6, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(b"\x00\xff\xff\xff\xff")) + chunk(b"IEND", b"")


def evidence(path, symbol, supports):
    return [{"path": path, "symbol": symbol, "supports": supports}]


def foundation(kind="service"):
    filename = "service.py" if kind == "service" else "linear_model.py"
    if kind == "service":
        modules = [
            ("M_REQUEST", "Request Handler", "component", "Pass the request key to the service.", "handle_request"),
            ("M_SERVICE", "Lookup Service", "component", "Normalize the key and assemble the response.", "LookupService.lookup"),
            ("M_STORE", "Memory Store", "store", "Look up a value in the in-memory mapping.", "MemoryStore.get"),
        ]
        edges = [
            ("E_REQUEST", "M_REQUEST", "M_SERVICE", "call", "Pass the request key.", "handle_request"),
            ("E_LOOKUP", "M_SERVICE", "M_STORE", "data", "Pass the normalized key for lookup.", "LookupService.lookup"),
            ("E_VALUE", "M_STORE", "M_SERVICE", "data", "Return the stored value.", "LookupService.lookup"),
            ("E_RESPONSE", "M_SERVICE", "M_REQUEST", "data", "Return the assembled key/value response.", "handle_request"),
        ]
        summary = "An injected in-memory store supports a normalized key lookup."
    else:
        modules = [
            ("M_MODEL", "Shared Linear Model", "component", "Predict with one shared weight and bias.", "LinearModel.forward"),
            ("M_TRAIN", "Training Step", "component", "Compute error and loss, then update the model parameters explicitly.", "train_step"),
            ("M_PREDICT", "Inference", "component", "Read the same model through forward without updates.", "predict"),
        ]
        edges = [
            ("E_TRAIN", "M_TRAIN", "M_MODEL", "call", "Evaluate the model on the training input.", "train_step"),
            ("E_PREDICTION", "M_MODEL", "M_TRAIN", "data", "Return a prediction used to compute error and loss.", "train_step"),
            ("E_UPDATE", "M_TRAIN", "M_MODEL", "state_update", "Update the same weight and bias using the explicit error-based gradients.", "train_step"),
            ("E_INFER", "M_PREDICT", "M_MODEL", "call", "Evaluate the shared model without parameter updates.", "predict"),
        ]
        summary = "Training mutates the parameters of the same model used for inference."
    return {
        "schema_version": "1.0", "analysis_id": "A01", "summary": summary,
        "source": {"label": kind, "revision": None, "working_tree": "unknown", "scope": [filename], "excluded": []},
        "modules": [{"id": mid, "label": label, "kind": mtype, "responsibility": responsibility,
                     "evidence": evidence(filename, symbol, responsibility)} for mid, label, mtype, responsibility, symbol in modules],
        "relationships": [{"id": eid, "source": src, "target": dst, "kind": etype, "meaning": meaning,
                           "certainty": "observed", "evidence": evidence(filename, symbol, meaning)}
                          for eid, src, dst, etype, meaning, symbol in edges],
        "groups": [], "flows": [], "terms": [], "uncertainties": [],
    }


class RunTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="c2a-test-")
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.run = self.base / "run"
        self.run.mkdir()
        self.source = self.base / "source"
        shutil.copytree(ROOT / "tests/fixtures", self.source)
        self.spec = foundation()
        self.write_json("analysis/A01/architecture-spec.json", self.spec)
        self.write("analysis/A01/code-analysis.md", "The handler calls the lookup service, which normalizes the key and uses its injected memory store.\n")
        self.write("candidate-plan.md", "C01 shows the component boundary; C02 can expand normalization.\n")
        self.manifest = {
            "schema_version": "1.0", "project_id": "fixture-service", "active_stage": "S2",
            "current_analysis_id": "A01", "analyses": [{"id": "A01", "report": "analysis/A01/code-analysis.md", "spec": "analysis/A01/architecture-spec.json"}],
            "candidate_plan": "candidate-plan.md", "candidates": [], "final": None,
        }
        self.add_version()

    def write(self, name, content):
        path = self.run / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content) if isinstance(content, bytes) else path.write_text(content, encoding="utf-8")
        return path

    def write_json(self, name, data):
        return self.write(name, json.dumps(data, indent=2))

    def add_version(self, cid="C01", vid="v01", refs=False):
        prefix = f"candidates/{cid}/{vid}/"
        prompt = (
            "Create a component architecture diagram of the implemented key lookup service.\n"
            "All visible text must be in English. Use Comic Sans MS for all visible text.\n"
            "Show Request Handler at the left, Lookup Service in the center, and Memory Store at the right.\n"
            "Request Handler passes the request key to Lookup Service. Inside Lookup Service, show normalization before lookup.\n"
            "Lookup Service sends the normalized key to Memory Store; a separate return arrow carries the stored value back.\n"
            "Lookup Service returns the assembled response to Request Handler through a separate return connection.\n"
            "Only show the labels Request Handler, Lookup Service, Memory Store, Normalize Key, Key, Value, and Response.\n"
            "Use a wide horizontal layout, a restrained teal accent for the service, and neutral gray for the store.\n"
            "Keep the return arrow below the forward path and all labels unobstructed. Do not imply a network database or an extra service.\n"
        )
        references = []
        guide = "# Reference guide\n\n[Complete prompt](architecture-prompt.md)\n\nNo image has been reviewed.\n"
        if refs:
            prompt += "Use Reference Image 1 only for spacing; the architecture and labels above are authoritative. Without it, follow the full text layout.\n"
            self.write(prefix + "references/layout.png", tiny_png())
            references = [{"id": "R1", "path": prefix + "references/layout.png", "origin": "user", "borrow": ["spacing"], "avoid": ["unrelated labels"]}]
            guide += "\nR1 / Reference Image 1: [Layout](references/layout.png); borrow spacing only.\n"
        self.write(prefix + "architecture-prompt.md", prompt)
        self.write(prefix + "reference-guide.md", guide)
        version = {"id": vid, "analysis_id": "A01", "status": "awaiting_images", "prompt": prefix + "architecture-prompt.md",
                   "reference_guide": prefix + "reference-guide.md", "reference_images": references, "returned_images": [], "reviews": [], "change_note": "Fixture candidate."}
        candidate = next((c for c in self.manifest["candidates"] if c["id"] == cid), None)
        if candidate is None:
            candidate = {"id": cid, "versions": []}
            self.manifest["candidates"].append(candidate)
        candidate["versions"].append(version)
        return version

    @property
    def version(self):
        return self.manifest["candidates"][0]["versions"][0]

    def check(self):
        self.write_json("manifest.json", self.manifest)
        return validate_run(self.run, self.source)

    def return_image(self, version=None, image_id="I01"):
        version = version or self.version
        path = f"returned-images/C01/{version['id']}/{image_id}.png"
        self.write(path, tiny_png())
        version["returned_images"].append({"id": image_id, "path": path, "origin": "human"})
        version["status"] = "images_received"

    def finalize(self, version=None):
        version = version or self.version
        refs = copy.deepcopy(version["reference_images"])
        for ref in refs:
            copied = "final/references/" + Path(ref["path"]).name
            self.write(copied, (self.run / ref["path"]).read_bytes())
            ref["path"] = copied
        self.write("final/architecture-prompt.md", (self.run / version["prompt"]).read_bytes())
        self.write("final/reference-guide.md", (self.run / version["reference_guide"]).read_bytes())
        self.manifest["active_stage"] = "S5"
        self.manifest["final"] = {"candidate_id": "C01", "version_id": version["id"], "analysis_id": version["analysis_id"],
                                  "selection_basis": "requested_prompt_only", "prompt": "final/architecture-prompt.md",
                                  "reference_guide": "final/reference-guide.md", "reference_images": refs}

    def test_prompt_only_handoff_allows_multiple_candidates_without_images(self):
        self.add_version("C02")
        self.finalize()
        result = self.check()
        self.assertEqual(result["candidates"], 2)
        self.assertEqual(result["returned_images"], 0)
        self.assertTrue(result["final_package"])

    def test_reference_package_remains_portable_after_moving_run(self):
        version = self.add_version(vid="v02", refs=True)
        self.finalize(version)
        self.check()
        moved = self.base / "moved"
        shutil.copytree(self.run, moved)
        self.assertTrue(validate_run(moved, self.source)["final_package"])

    def test_review_and_revision_keep_original_image_association(self):
        self.return_image()
        self.write("reviews/C01-v01-review.md", "Fixture human observation: the Value return arrow points the wrong way; reverse it in v02.\n")
        self.version["reviews"] = [{"path": "reviews/C01-v01-review.md", "image_ids": ["I01"], "basis": "human_observations"}]
        self.version["status"] = "reviewed"
        revision = self.add_version(vid="v02", refs=True)
        revision["reference_images"][0].update({"origin": "returned_image", "source_candidate_id": "C01", "source_version_id": "v01", "source_image_id": "I01"})
        self.finalize(revision)
        self.assertEqual(self.check()["versions"], 2)
        self.assertEqual(self.version["returned_images"][0]["id"], "I01")

    def test_missing_attachment_is_rejected(self):
        version = self.add_version(vid="v02", refs=True)
        (self.run / version["reference_images"][0]["path"]).unlink()
        with self.assertRaisesRegex(ValidationError, "missing file"):
            self.check()

    def test_attachment_numbers_must_match_prompt(self):
        version = self.add_version(vid="v02", refs=True)
        path = self.run / version["prompt"]
        path.write_text(path.read_text().replace("Reference Image 1", "Reference Image 2"))
        with self.assertRaisesRegex(ValidationError, "reference numbers"):
            self.check()

    def test_review_cannot_claim_an_unreturned_image(self):
        self.version["status"] = "reviewed"
        with self.assertRaisesRegex(ValidationError, "without images"):
            self.check()

    def test_review_must_cover_each_returned_image(self):
        self.return_image()
        self.return_image(image_id="I02")
        self.write("reviews/one.md", "Fixture review of I01 only.")
        self.version["reviews"] = [{"path": "reviews/one.md", "image_ids": ["I01"], "basis": "direct"}]
        self.version["status"] = "reviewed"
        with self.assertRaisesRegex(ValidationError, "all returned images"):
            self.check()

    def test_review_cannot_point_to_another_version_image(self):
        self.return_image()
        revision = self.add_version(vid="v02")
        self.write("reviews/wrong.md", "Fixture with an incorrect association.")
        revision["reviews"] = [{"path": "reviews/wrong.md", "image_ids": ["I01"], "basis": "direct"}]
        with self.assertRaisesRegex(ValidationError, "wrong candidate/version"):
            self.check()

    def test_empty_review_file_does_not_count_as_a_completed_review(self):
        self.return_image()
        self.write("reviews/empty.md", "")
        self.version["reviews"] = [{"path": "reviews/empty.md", "image_ids": ["I01"], "basis": "direct"}]
        self.version["status"] = "reviewed"
        with self.assertRaisesRegex(ValidationError, "review report"):
            self.check()

    def test_final_content_drift_requires_a_new_version(self):
        self.finalize()
        self.write("final/architecture-prompt.md", "Changed without a candidate version.")
        with self.assertRaisesRegex(ValidationError, "differs from selected version"):
            self.check()

    def test_final_cannot_silently_select_an_outdated_foundation(self):
        self.finalize()
        updated = copy.deepcopy(self.spec)
        updated["analysis_id"] = "A02"
        self.write_json("analysis/A02/architecture-spec.json", updated)
        self.write("analysis/A02/code-analysis.md", "Updated foundation.")
        self.manifest["analyses"].append({"id": "A02", "report": "analysis/A02/code-analysis.md", "spec": "analysis/A02/architecture-spec.json"})
        self.manifest["current_analysis_id"] = "A02"
        with self.assertRaisesRegex(ValidationError, "current analysis"):
            self.check()

    def test_paths_cannot_escape_the_run_through_a_symlink(self):
        outside = self.base / "outside.md"
        outside.write_text("External file")
        path = self.run / self.version["prompt"]
        path.unlink()
        path.symlink_to(outside)
        with self.assertRaisesRegex(ValidationError, "escapes its root"):
            self.check()

    def test_prompt_requires_fixed_font_and_english(self):
        path = self.run / self.version["prompt"]
        original = path.read_text()
        for changed, expected in [(original.replace("Comic Sans MS", "Helvetica"), "Comic Sans MS"), (original + "额外标签", "non-English")]:
            with self.subTest(expected=expected):
                path.write_text(changed)
                with self.assertRaisesRegex(ValidationError, expected):
                    self.check()

    def test_prompt_cannot_delegate_content_to_internal_spec(self):
        path = self.run / self.version["prompt"]
        path.write_text(path.read_text() + "Read architecture-spec.json for the remaining connections.")
        with self.assertRaisesRegex(ValidationError, "internal analysis"):
            self.check()

    def test_dangling_edge_and_unsupported_inference_are_rejected(self):
        bad = copy.deepcopy(self.spec)
        bad["relationships"][0]["target"] = "M_MISSING"
        with self.assertRaisesRegex(ValidationError, "dangling"):
            validate_spec(bad, self.source)
        bad = copy.deepcopy(self.spec)
        bad["relationships"][0]["certainty"] = "inferred"
        with self.assertRaisesRegex(ValidationError, "derivation"):
            validate_spec(bad, self.source)

    def test_source_anchors_are_checked_against_current_checkout(self):
        bad = copy.deepcopy(self.spec)
        bad["modules"][0]["evidence"][0]["path"] = "missing.py"
        with self.assertRaisesRegex(ValidationError, "missing file"):
            validate_spec(bad, self.source)
        bad = copy.deepcopy(self.spec)
        bad["modules"][0]["evidence"][0]["lines"] = [1, 1000]
        with self.assertRaisesRegex(ValidationError, "exceeds source"):
            validate_spec(bad, self.source)

    def test_training_and_inference_can_share_model_with_distinct_edge_types(self):
        spec = foundation("model")
        validate_spec(spec, self.source)


if __name__ == "__main__":
    unittest.main()
