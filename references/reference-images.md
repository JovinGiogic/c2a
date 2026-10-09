# Selecting and handing off reference images

Reference images are optional visual inputs. A candidate remains fully specified by its prompt; the reference supplies appearance or a local visual convention rather than missing architecture facts.

## Find and inspect

Use [the asset guide](../assets/README.md) and [reference index](../assets/reference-index.jsonl). Search by code roles and topology first, then by visual treatment. Read only relevant entries, rather than loading the entire library into context.

The optional `scripts/find_references.py` helper returns asset IDs, titles, preview/source paths, tags, borrowing limits, and provenance. Relative library paths are based at the installed skill directory. Resolve them there before copying an attachment.

Inspect the actual selected preview when image viewing is available. A filename or tag alone does not prove suitability. Without visual capability, describe matches as metadata-based suggestions and ask the human to verify them if suitability matters. User-provided reference images follow the same rules.

Choose an explicit role for each reference:

- overall layout or reading order;
- visual treatment, shape, or color inspiration;
- a local icon or mechanism motif;
- a previous returned candidate whose useful appearance the human wants to preserve.

Borrow only relevant aspects. Never copy unrelated module names, labels, datasets, metrics, unsupported topology, or factual claims. Fixed English text and Comic Sans MS override the reference's text and font. Reference colors and geometry are adopted only when appropriate for the target design.

## Self-contained prompts with attachments

In the prompt, write a complete text description of the desired figure, then add bounded reference instructions, for example:

```text
Use Reference Image 1 only as inspiration for its role-lane grouping and spacing.
The architecture, connections, and English labels specified in this prompt are authoritative.
Render all visible text in Comic Sans MS. Do not copy the reference's labels or add its modules.
If the reference image is unavailable, follow the complete textual layout description below.
```

Use `Reference Image 1` for manifest reference ID `R1`, `Reference Image 2` for `R2`, and so on. Use consecutive IDs starting at R1 within each candidate version. Do not put local source paths or retrieval-index instructions in the image prompt.

## Human handoff

Copy each selected uploadable preview into `candidates/<candidate>/<version>/references/` and write `reference-guide.md` in the user's language using [the template](../templates/reference-guide-template.md). Prepare the run's `returned-images/<candidate>/<version>/` directory as a usable return destination; keep manifest image records empty until real images arrive. If filesystem writing is unavailable, give the exact intended path and ask the human to create it when saving. The guide includes:

1. Candidate ID, prompt version, and analysis ID.
2. A clickable link to the complete prompt and its measured length, at most 7000 characters.
3. Each reference ID, attachment order, a clickable relative file link, and its asset/source identifier.
4. What to borrow, what to avoid, and whether the image has been visually inspected.
5. Generation steps: open the prompt, copy its entire text, upload the listed attachments in order when supported, and generate externally.
6. The actual run directory and full result-save path, distinct filenames such as `result-01.png`, and a relative link to the prepared return directory when available. Explain that users who cannot save there can upload the image in the conversation or supply an accessible file path.
7. A ready-to-copy return message containing the real candidate/version and image path, plus instructions to disclose any prompt edits and optionally state what to preserve or improve. Explain that review can produce a new complete prompt and guide for another round.

The manifest stores paths relative to the run root; links in a guide are relative to that guide. These two bases must not be confused. For example, the manifest might store `candidates/C01/v01/references/layout.png`, while the neighboring guide links to `references/layout.png`. The return destination is `returned-images/C01/v01/` from the run root, `../../../returned-images/C01/v01/` from that candidate guide, and `../returned-images/C01/v01/` from the final guide when C01/v01 is selected. Resolve the human-facing full path against the actual workspace, and update it if the run moves. Link only to directories that exist; when delivering text-only artifacts or only a detached `final/` package, use a plain destination path and the upload alternative instead of a broken link.

When there are no references, replace the attachment table with “No reference images are required; use the complete text prompt,” keep `reference_images` empty, and retain the generation and return instructions. Do not invent a reference to satisfy a template. When the chosen generator cannot accept reference images, the full text prompt remains usable; do not start a provider-configuration workflow.

At every prompt delivery, revision, and final handoff, **explicitly direct the human to open the guide**. Lead the response with a clickable link to the actual guide and a short next action in the user's language: follow it to submit the prompt and attachments, generate externally, then save or upload the result with its candidate/version for review. Also link the complete prompt. For a prompt-only request, explain that generation and return are optional.

## Retained assets and portability

Library PNGs are prepared previews of existing material. Original vector or presentation files can be retained for provenance and reuse. A source SVG or presentation file alone is not a portable image attachment: prefer its existing PNG preview. Preparing a faithful crop/export of an existing reference is asset maintenance, not generation of the target architecture.

Retain source and license information with selected assets. Historical source-paper identifiers are provenance only. Missing historical originals must never be listed as local available attachments.

At final handoff, copy the selected attachments into `final/references/`, preserve their IDs/order, and rewrite the guide's prompt, attachment, and return-directory links. Keep the return location associated with the selected candidate/version; there is no separate `final` candidate. The prompt and its reference attachments must remain usable independently of the installed skill's location or a previous candidate directory.
