# Reference image library

Use these existing images to support architecture-figure design and human image-generation handoffs. They are references, not outputs for the code project being analyzed.

## Contents

The [line-oriented catalog](reference-index.jsonl) contains 1,064 searchable records:

| Kind | Records | Intended use |
| --- | --- | --- |
| `atlas` | 4 | Compare layout, reader emphasis, and visual treatment. Select a relevant aspect rather than copying an entire multi-panel board. |
| `concept` | 60 | High-level model and algorithm arrangements exported from the retained concept presentation. |
| `icon` | 407 | Curated local icon shapes for architectural roles. |
| `motif` | 100 | Curated local mechanisms and structural patterns. |
| `primitive` | 493 | Curated building blocks for model, data, and agent diagrams. |

Every record has an actual PNG `preview_path`, a retained `source_path`, tags, borrowing limits, and provenance. Identical vector files share a canonical source/preview while their different semantic aliases remain searchable. The catalog contains 815 distinct PNG previews and 751 distinct vector sources, plus one editable concept presentation.

## Search and selection

From the skill directory:

```bash
python scripts/find_references.py "training inference shared model" --limit 6
python scripts/find_references.py "retrieval" --kind concept --limit 4
```

An Agent can also search `reference-index.jsonl` directly. Catalog paths are relative to the skill root, not to this file or the analyzed repository. Search output omits long historical source lists by default; add `--details` when provenance detail is needed. Retrieval is a starting point; inspect selected previews and compare their actual structure with the code before recommending them.

Examples:

- [Visual grammar and layout](reference-library/boards/visual-grammar-layout.png)
- [Visual communication styles](reference-library/boards/visual-communication-styles.png)
- [Shared transformer-block concept](reference-library/concepts/concept.transformer_block.png)
- [Retrieval pipeline concept](reference-library/concepts/concept.rag_pipeline.png)

## Delivery

Copy selected PNG previews into the candidate's `references/` directory. Record the asset ID, attachment number, actual file link, borrowing scope, and limitations in `reference-guide.md`. Follow [reference-images.md](../references/reference-images.md).

Reference text and fonts may differ from the target standard. The new figure's prompt must still specify English visible text and Comic Sans MS. Reference labels, colors, and topology do not establish facts about the target code.

Concept previews contain the original diagram objects with presentation titles, frames, and editing notes removed. Their original slides remain in [neural-concepts.pptx](reference-library/concepts/neural-concepts.pptx); `source_page` is a one-based slide number. Other PNGs are faithful exports of retained vector assets or original atlas boards. No image-generation service is used to prepare these previews.

## Maintenance

Keep a source file, a usable PNG preview, and provenance for each catalog entry. Remove duplicates only after updating all entries that share them. Do not register missing historical source figures as available attachments. Run `python scripts/validate_artifacts.py --package .` from the skill root after changes.

Source and usage information is in [ATTRIBUTION.md](ATTRIBUTION.md) and each record's `provenance` field.
