#!/usr/bin/env python3
"""Search the bundled reference catalog without loading every asset into an Agent."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys


KINDS = ("atlas", "icon", "motif", "primitive", "concept")
PACKAGE_ROOT = Path(__file__).resolve().parent.parent


def read_catalog(path: Path) -> list[dict]:
    entries = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        entry = json.loads(line)
        if not isinstance(entry, dict):
            raise ValueError(f"{path.name}:{number}: expected an object")
        entries.append(entry)
    return entries


def words(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", value.lower()))


def find_references(query: str, entries: list[dict], limit: int = 6,
                    kind: str | None = None) -> list[dict]:
    tokens = words(query)
    ranked = []
    for entry in entries:
        if kind and entry.get("kind") != kind:
            continue
        title = words(str(entry.get("title", "")))
        tags = words(" ".join(entry.get("tags", [])))
        context = words(" ".join(entry.get("borrow", [])))
        score = 5 * len(tokens & title) + 3 * len(tokens & tags) + len(tokens & context)
        if tokens and not score:
            continue
        ranked.append((score, entry))
    ranked.sort(key=lambda row: (-row[0], row[1].get("asset_id", "")))
    return [dict(entry, retrieval_score=score) for score, entry in ranked[:limit]]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="Architecture roles, topology, or visual terms")
    parser.add_argument("--kind", choices=KINDS)
    parser.add_argument("--limit", type=int, default=6)
    parser.add_argument("--details", action="store_true", help="Include the full historical source list for each match")
    parser.add_argument("--index", type=Path, default=PACKAGE_ROOT / "assets/reference-index.jsonl")
    args = parser.parse_args()
    if args.limit < 1:
        parser.error("--limit must be positive")
    try:
        results = find_references(args.query, read_catalog(args.index), args.limit, args.kind)
    except (OSError, ValueError, TypeError) as error:
        print(f"Reference search failed: {error}", file=sys.stderr)
        return 1
    if not args.details:
        results = [dict(row, provenance={k: v for k, v in row.get("provenance", {}).items()
                                        if k != "historical_sources"}) for row in results]
    print(json.dumps({"path_base": "skill_root", "matches": results}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
