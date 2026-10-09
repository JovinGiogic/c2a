# Shared architecture specification

Use [the JSON template](../templates/architecture-spec-template.json). The specification captures implemented meaning; the candidate plan decides how to render it. A semantic entity need not become a separate box in every candidate.

## Fields

| Field | Meaning |
| --- | --- |
| `schema_version` | `1.0`. |
| `analysis_id` | Stable ID such as `A01`, matching the manifest. |
| `source` | Repository label, revision or `null`, working-tree state, included scope, and exclusions. Paths here and in evidence are source-repository-relative. |
| `summary` | What the selected implementation does and what this figure can explain. |
| `modules` | Objects with unique `id`, English `label`, `kind`, `responsibility`, and `evidence`. Kinds: `component`, `external`, `store`, `artifact`, or `actor`. |
| `relationships` | Objects with unique `id`, `source`, `target`, `kind`, optional English `label`, `meaning`, `certainty`, and `evidence`. Endpoint values are module IDs. |
| `groups` | Optional containers with unique `id`, English `label`, member module IDs, and a `meaning`; grouping must not invent process/deployment boundaries. |
| `flows` | Named paths with unique `id`, English `label`, `phase`, ordered `module_ids`, and `relationship_ids`. Use the relationship records for exact topology; a listed path is not permission to add an edge. |
| `terms` | Mappings from `source_term` to English `display_label` and `meaning`. Preserve source-defined abbreviations and distinguish overloaded terms. |
| `uncertainties` | Objects with unique `id`, `question`, `impact`, `affected_ids`, and `resolution`. Unresolved central questions prevent a claim of complete scope. |

Relationship kinds are `call`, `data`, `control`, `event`, `state_update`, `training`, `dependency`, `ownership`, and `deployment`. Explain the specific meaning: e.g. a `data` edge transfers a query, a `state_update` edge writes a cache, a `training` edge supplies a loss. Use separate relations when direction or meaning actually differs, not for decorative parallel arrows.

Every evidence entry has:

```json
{
  "path": "src/service.py",
  "symbol": "Service.handle",
  "lines": [24, 38],
  "supports": "Passes the normalized query to the retriever."
}
```

`lines` is optional and inclusive. `symbol` may identify a class, function, route, configuration key, or module. Anchor paths must exist in the inspected source snapshot; do not use a deleted/missing file as evidence. External internals can be unknown while a local integration call is directly supported.

Relationship `certainty` is `observed` or `inferred`. An inferred relationship additionally requires `derivation`, explaining the evidence and inference. Put an unsupported possibility in `uncertainties` rather than the relation list.

## IDs and display labels

Use stable IDs such as `M_API`, `M_RETRIEVER`, and `E_QUERY`. All module, relationship, group, flow, and uncertainty IDs must be unique across the specification. IDs are internal; use English `label` values in the image prompt. Do not put source paths, analysis IDs, candidate IDs, JSON keys, or audit fields into visible figure text.

Group membership and flow references must resolve. Self-loops are allowed only when the meaning and evidence establish a real recurrent action. A static dependency and a runtime transfer between the same components may coexist, but the candidate must distinguish them or intentionally omit the less relevant one.

## Candidate-specific abstraction

Record in `candidate-plan.md` which components remain visible, which are grouped, which details become edge labels, and which are out of scope. Preserve required operations and meaningful boundaries. Any compressed path must correspond to real supported relations; collapsing a helper must not reverse direction or imply a false consumer.

An overview may omit internal relations that a mechanism-focused candidate expands. Explain the difference in scope. Every candidate still gives a complete description of its chosen scope and cannot borrow missing architecture from another candidate or a reference image.

## Changes and checks

Freeze each analysis under `analysis/<analysis_id>/`. When code, active configuration, scope, or interpretation changes, create a new analysis version, describe the delta, and recheck affected candidates. Historical prompts keep their original analysis ID.

The optional validator checks evidence paths (with `--source-root`), IDs, endpoints, and structural fields. It cannot establish whether a cited symbol supports the claim; that remains part of code reading and review.
