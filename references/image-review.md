# Reviewing human-returned images

## Establish what is being reviewed

Record the returned image's path, candidate ID, prompt version, and analysis ID. Read that version's complete prompt, attachment guide, and code foundation. If a human edited the prompt before generation, preserve the actual submitted prompt as a new version or record the known difference; do not claim the image was generated from an unchanged version without knowing that.

Several images may come from the same prompt. Give them distinct image IDs and review them separately. When the candidate/version association is unclear, ask the human before making version-specific findings. Never infer a prompt version from an image's appearance alone.

Use [the review template](../templates/review-template.md). State the review basis:

- `direct`: the reviewer accessed and visually inspected the image;
- `human_observations`: findings are based on observations supplied by the human. State which properties were not independently inspected.

Without image access or visual capability, continue useful text/code work, but do not fabricate image findings or a visual pass. Unreadable or ambiguous areas remain unverified.

## Review priorities

1. **Code fidelity:** actual modules, responsibilities, phases, shared/independent instances, state boundaries, and required core operations.
2. **Relations:** correct endpoints, direction, branch/merge behavior, connector meaning, and true consumers of data. Check for extra decorative arrows that imply nonexistent behavior.
3. **Text:** English labels, source-defined terms, missing/extra labels, spelling, internal IDs accidentally shown, and source paths or schema keys leaking into the figure.
4. **Typography:** Comic Sans MS requested for every visible text element. Record `appears_consistent`, `mismatch`, or `unverified`; a raster impression alone is not exact font identification.
5. **Visual communication:** reading order, meaningful grouping, focus, legibility, density, contrast, overlap, repeated structures, and clarity at the intended viewing size.
6. **Reference transfer:** useful visual aspects adopted without copying irrelevant modules, text, colors with conflicting meaning, or unsupported topology.

## Issue records

Give each issue an ID, severity (`minor`, `moderate`, `major`, `blocker`), image/region, observed problem, code/spec/prompt evidence, likely cause, and concrete prompt correction. Mark the cause as `code_understanding`, `prompt_ambiguity`, `rendering_deviation`, or `unknown`. A correction is a hypothesis when the cause cannot be established.

Separate severity from ease of correction. A small reversed arrow can be a major error; a large visual change can be merely stylistic. Record useful aspects worth preserving as well as defects. Do not let aesthetic preference overrule an unsupported architecture.

Report what was checked, what remains uncertain, and what the human needs to decide. Recommend a candidate or combination when requested, with code fidelity and unresolved issues made clear. Do not call an image fully verified when observations were indirect or important areas were unreadable.

## Refinement

- If code understanding was wrong, correct the foundation under a new analysis ID and reassess affected candidate semantics.
- If presentation or prompt clarity was wrong, keep the analysis ID and write a new candidate version.
- Preserve user-selected useful features and explain any that must change to stay faithful to code.
- Turn specific defects into precise positive instructions and targeted prohibitions, rather than accumulating generic negative wording.
- Write a complete replacement prompt with English text, Comic Sans MS, and its own reference mapping. It must work without the previous prompt.
- A returned image may become a new reference for its useful appearance. Copy it into the new version's attachments, identify its origin, and explicitly prohibit carrying forward the defects found in review.

After delivering the revision, the next image-generation step belongs to the human. Preserve the current result and wait for a returned image if further visual review is requested.
