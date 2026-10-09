# Run artifacts and version correspondence

Keep run outputs outside the installed skill. Use [manifest-template.json](../templates/manifest-template.json) as a small index, not a workflow engine. All manifest file paths are relative to the run root. Source-evidence paths are relative to the analyzed repository. Library-index paths are relative to the skill root. Markdown links are relative to their containing document.

## Layout

```text
analysis/A01/code-analysis.md
analysis/A01/architecture-spec.json
candidate-plan.md
candidates/C01/v01/architecture-prompt.md
candidates/C01/v01/reference-guide.md
candidates/C01/v01/references/layout.png
returned-images/C01/v01/result-01.png
reviews/C01-v01-I01-review.md
manifest.json
final/architecture-prompt.md
final/reference-guide.md
final/references/layout.png
```

Directories and optional files are created only when needed. Do not make empty image/review/final artifacts to imply progress. An image prompt can be complete without any returned image.

## Manifest fields

| Field | Contract |
| --- | --- |
| `schema_version` | `1.0`. |
| `project_id` | A nonempty stable project label. |
| `active_stage` | `S0` through `S5`, indicating the current work/handoff context. |
| `current_analysis_id` | Current foundation ID or `null` while analysis is not ready. |
| `analyses` | List of `{id, report, spec}`. Each spec's `analysis_id` must match. Freeze versions under `analysis/<id>/`. |
| `candidate_plan` | Run-relative plan path, or `null` before design. |
| `candidates` | List of `{id, versions}` with unique IDs. |
| `final` | `null`, or the selected final package record described below. |

Each candidate version contains:

```json
{
  "id": "v01",
  "analysis_id": "A01",
  "status": "awaiting_images",
  "prompt": "candidates/C01/v01/architecture-prompt.md",
  "reference_guide": "candidates/C01/v01/reference-guide.md",
  "reference_images": [
    {
      "id": "R1",
      "path": "candidates/C01/v01/references/layout.png",
      "origin": "library",
      "asset_id": "atlas.visual-grammar-layout",
      "borrow": ["role-lane grouping"],
      "avoid": ["reference labels and unsupported connections"]
    }
  ],
  "returned_images": [],
  "reviews": [],
  "change_note": "Initial candidate."
}
```

Version statuses are `draft`, `ready`, `awaiting_images`, `images_received`, `reviewed`, and `superseded`. A draft can have `null` prompt/guide paths; every declared non-null path must exist. Other statuses require a complete prompt and guide. `images_received` requires a returned image. `reviewed` requires review coverage of every returned image; the review basis must still be disclosed.

Reference IDs are consecutive `R1`, `R2`, etc., matching the prompt's `Reference Image 1`, etc. Each reference requires `id`, `path`, `origin`, `borrow`, and `avoid`. `origin` is `library`, `user`, or `returned_image`. Library entries additionally need `asset_id`; returned-image references need `source_candidate_id`, `source_version_id`, and `source_image_id`. Copy image files into the new version rather than linking to mutable external locations.

A returned image record is `{id, path, origin: "human"}`. IDs are unique within the candidate version. A review record is `{path, image_ids, basis}`, where `basis` is `direct` or `human_observations` and image IDs belong to this exact version. A human-observation review is valid documentation but is not independent visual verification.

`change_note` describes what changed and why, including source interpretation changes, preferences preserved, and changed reference attachments. Do not overwrite the prompt or reference set of a version that already has returned images.

## Final package

```json
{
  "candidate_id": "C01",
  "version_id": "v02",
  "analysis_id": "A01",
  "selection_basis": "human_choice",
  "prompt": "final/architecture-prompt.md",
  "reference_guide": "final/reference-guide.md",
  "reference_images": []
}
```

`selection_basis` is `human_choice` or `requested_prompt_only`. The final prompt is a copy of the selected version; if its content needs to change, create a new candidate version first. Copy the selected attachments into `final/references/` using the same IDs, and update the final guide's links. The final reference records use the same structure as candidate references with final-relative file locations. Record the actual review state in the guide; selection alone does not certify an image.

Finalization normally uses the current analysis. If the chosen candidate predates a meaning-changing foundation revision, recheck it against the current foundation and create a new version before finalization. Historical candidates retain their original analysis association.

## Resume and validate

On resumption, read the manifest, current foundation, relevant candidate version, and existing reviews. Check source/scope changes. Do not repeat completed work solely because a new conversation began, and do not infer that external generation happened without a returned image.

The optional validator checks IDs, files, references, graph endpoints, basic prompt language/font requirements, and final-package correspondence. With `--source-root`, it checks current-analysis evidence files and line bounds; historical snapshots are not validated against a changed checkout. File existence and structural consistency do not prove source fidelity or visual quality.
