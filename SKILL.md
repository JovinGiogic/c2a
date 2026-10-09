---
name: c2a
description: Analyze a code repository to design evidence-based architecture figures, deliver self-contained English image prompts with optional reference images, and review human-generated images to refine those prompts. Use for code architecture, model structure, execution pipelines, or agent workflows. Image generation is performed by the human outside this skill.
---

# C2A — Code to Architecture

Turn implemented code into accurate architecture-figure prompts. Preserve the code analysis, candidate alternatives, reference attachments, and review history alongside the final `architecture-prompt.md`.

## Working boundary

- Read the accessible repository, relevant configuration, and project documentation. Follow entry points and actual wiring; a directory tree or import graph alone is not an architecture.
- Use the host Agent's file reading, search, and text-writing capabilities. No particular model, host, browser, image provider, or runtime is required. The Python helpers are optional checks, not prerequisites.
- Resolve this skill's scripts, templates, references, and assets relative to this `SKILL.md`, even when the working directory is the code repository.
- If file writing is unavailable, deliver named artifact blocks for the human to save and identify accessible reference files honestly. Do not claim a file or portable package exists until it has actually been saved.
- The human generates images externally and returns them. Do not call an image-generation tool or API, request image credentials, or render the target architecture yourself.
- Visual review requires access to the returned image and visual capability. Otherwise record human observations as such and leave unobserved properties unverified.
- Keep project outputs outside the installed skill, normally under `c2a-runs/<project>/` in a chosen workspace. Read source code without starting the application, installing its dependencies, or changing it merely to draw its architecture.

## Fixed standards

1. Write the image prompt itself in **English**. All visible titles, module labels, edge labels, annotations, and legends must be English; preserve necessary source-defined identifiers and mathematical notation.
2. Specify **Comic Sans MS for all visible text** in every prompt, including revisions. Reference images do not override this font or the English-language requirement.
3. Make every prompt self-contained: include the complete architecture, exact visible labels, relationships, layout instructions, and constraints. A downstream generator must not need the code, an analysis report, another prompt, or an internal schema.
4. Optional attachments may supplement the visual description. Identify them as `Reference Image 1`, etc.; give the human their real paths and borrowing limits in `reference-guide.md`. No attachment is the sole specification of architecture facts.
5. Ground all architecture claims in the selected code/configuration. Distinguish observed relationships, justified inferences, and unknowns. Never invent a component or edge to improve the layout.
6. Choose theme, layout, palette, aspect ratio, detail, and reference material for the particular project. Explain the choice; do not impose a universal palette, canvas, or diagram topology. The font does not dictate a cartoon or hand-drawn theme.

Analysis, plans, reviews, and conversation may use the user's language.

## Workflow

Keep these stages visible, and honor requests for staged confirmation. When authorized, analysis and design can continue through prompt delivery. Pause at external image generation until the human returns images; do not fabricate that step or its review. A prompt-only request can finish at delivery without requiring an image.

| Stage | Work | Deliverables / handoff |
| --- | --- | --- |
| S0 — Code foundation | Establish scope, read code, record evidence, separate architecture facts from uncertainties. | `analysis/A01/code-analysis.md`, `analysis/A01/architecture-spec.json`, ready for human correction. |
| S1 — Candidate design | Choose reader questions, levels of detail, and genuinely different visual approaches; retrieve suitable references. | `candidate-plan.md`, including candidate IDs, reasons, and proposed references. |
| S2 — Prompt delivery | Write and check each complete prompt, copy selected reference previews, and explain the attachment mapping. | `candidates/C01/v01/architecture-prompt.md`, `reference-guide.md`, optional `references/`. The human can take these to any compatible image tool. |
| S3 — Returned-image review | Match returned images to candidate/version, then compare the actual image with the code foundation and prompt. | Images under `returned-images/`; evidence-based reports under `reviews/`. |
| S4 — Prompt refinement | Correct issues and incorporate the human's preferences without changing code facts. | A new candidate version with a complete prompt, reference guide, and change note. Return to human generation, then S3, as needed. |
| S5 — Final handoff | Package the version selected by the human, or the explicitly requested prompt-only deliverable. | `final/architecture-prompt.md`, `final/reference-guide.md`, and the selected attachments. Preserve analysis and candidate history. |

Candidate count follows the request and the number of useful alternatives. Two or three distinct approaches are often helpful; do not manufacture alternatives or impose a fixed two-round quota. Each candidate can be delivered or revised independently.

### S0: understand before designing

Read [code-reading.md](references/code-reading.md) and use the [analysis template](templates/code-analysis-template.md). Record the source snapshot, entry/configuration choices, coverage, modules, execution paths, and evidence. Use [architecture-model.md](references/architecture-model.md) and the [specification template](templates/architecture-spec-template.json) for the shared structural foundation.

Show the foundation to the human for reference and correction. Resolve uncertainties that change the requested main architecture before claiming a complete foundation; otherwise explicitly narrow the scope or mark the uncertainty. Do not present a conjecture as implemented behavior.

### S1–S2: design and deliver

Read [visual-design.md](references/visual-design.md), [reference-images.md](references/reference-images.md), and [prompt-writing.md](references/prompt-writing.md). Use the [candidate plan](templates/candidate-plan-template.md), [prompt](templates/architecture-prompt-template.md), and [reference guide](templates/reference-guide-template.md) templates.

Search the [reference index](assets/reference-index.jsonl) only when references would help. Optional helper:

```bash
python scripts/find_references.py "retrieval memory agent" --limit 6
```

Inspect the chosen preview before claiming visual suitability; if visual inspection is unavailable, label it an unverified suggestion for the human. Copy selected previews into the candidate package. References can guide layout, visual treatment, or a local motif, but cannot supply unsupported modules, labels, or arrows.

Deliver the complete prompt file and attachment guide, not an instruction to run another stage. Distinguish “prompt checked” from “image reviewed.”

### S3–S4: review what was actually returned

Read [image-review.md](references/image-review.md) and use the [review template](templates/review-template.md). Associate each returned image with its candidate and prompt version; ask for the mapping when it cannot be determined. Never infer it from appearance alone.

Record specific issues, image locations, evidence, severity, and the corresponding prompt repair. Distinguish code-understanding errors, prompt ambiguities, and rendering deviations. Font identity or unreadable labels may be unverified; do not claim exact compliance from an uncertain visual impression.

If the foundation changes, create a new analysis version and mark affected candidates for rechecking. If only presentation changes, preserve the foundation. Write each revision in a new version directory; it must contain the full prompt and its own attachment mapping, not just editing instructions.

### S5: make the handoff portable

Copy the chosen prompt, guide, and attachments into `final/`, adjusting the guide's relative links. Record the selection and whether its image was reviewed. A prompt-only final is valid but must not be called an approved or verified image. The human may later return an image and resume review.

## Lightweight recordkeeping

Use [artifact-contract.md](references/artifact-contract.md) and [manifest-template.json](templates/manifest-template.json). Keep one manifest linking analysis versions, candidates, prompt versions, reference images, returned images, and reviews. No checkpoint archive is required.

All artifact paths in a manifest are relative to the run directory; source anchors are relative to the analyzed repository. Preserve previous versions. Reuse existing artifacts when resuming, and check whether the source snapshot or scope changed.

Optional checks, from the skill directory:

```bash
python scripts/validate_artifacts.py --package .
python scripts/validate_artifacts.py --run /path/to/c2a-runs/project --source-root /path/to/source
```

These check structure, files, IDs, references, and basic prompt requirements. They do not prove semantic accuracy, English fluency, visual quality, or exact font rendering. Perform the relevant code and visual review as well.
