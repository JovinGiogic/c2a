# Writing and checking architecture prompts

Use [the prompt template](../templates/architecture-prompt-template.md). Replace every placeholder, expand the architecture explicitly, and remove irrelevant sections. A delivered file contains the complete English image prompt, without workflow commands or human-only commentary.

## Content

1. **Purpose and scope:** the implemented system and the reader's main takeaway.
2. **Fixed typography:** all visible text is English; all visible text uses Comic Sans MS.
3. **Architecture:** visible modules, groups, internal mechanisms, and any actual phase/instance distinctions. Use English display labels, not specification IDs.
4. **Exact connections:** describe source, destination, direction, meaning, and optional visible label for every required connector. Include branch, loop, shared-state, and port rules where relevant.
5. **Visible text:** list the exact permitted labels by role. State that internal identifiers, source paths, audit terms, and extra invented labels must not be drawn.
6. **Layout and treatment:** reading order, placement, hierarchy, chosen palette, shapes, line conventions, aspect ratio, and density, justified in the candidate plan and fully described here.
7. **Optional references:** attachment numbers, narrow borrowing instructions, and a complete text fallback. Omit this section when there are no attachments.
8. **Project-specific constraints:** likely architectural misreadings to prevent, required details not to drop, and legibility constraints.

The image generator receives this file and optional attachments, not `architecture-spec.json` or a source repository. Therefore, "follow A01", "same as the last prompt", "read the code", or a path to another specification cannot stand in for architecture or layout content. A revision must restate everything still required, including typography and reference instructions.

## Meaning before appearance

Compile connections from the shared architecture specification and the candidate's selected abstraction. Distinguish call, data, control, state, and other relation types when their distinction matters. Do not let a shape, placement, icon, or reference image invent a module, consumer, branch, process boundary, or return path.

Show variables as labels/ports when they are carried quantities; show stores, queues, and important artifacts as objects when their role warrants it. Label compression must not merge different concepts or disguise repeated instances as one shared object. Preserve core operations even in a simplified overview.

Use English visible labels mapped to code terms. Do not translate or expand an acronym into an unsupported meaning. Mathematical notation and source-defined identifiers can remain where needed, with English explanatory labels.

## Before delivery

Check the prompt against its exact analysis ID, candidate plan, and attachment set:

- Main modules and required mechanisms are covered at the intended abstraction.
- Every connector is supported, correctly directed, and carried by a real producer/consumer relationship.
- Labels are complete, consistent, English, and separate from internal IDs.
- Comic Sans MS is specified for all visible text; there is no conflicting font instruction.
- Theme, layout, palette, and density suit the project and agree with each other.
- Reference numbers resolve to real copied attachments and state their limited role.
- The prompt stands alone, has no placeholders, and is a complete revision rather than a patch instruction.

Repair contradictions before calling a prompt ready. If a central source ambiguity remains, resolve it or narrow the claim instead of hiding it with a visual instruction. Do not loop indefinitely: explain the missing fact and preserve the partial work for the human when it cannot be resolved from the available code.

The optional validator checks basic format and reference correspondence. It cannot prove English fluency or that every architectural statement is supported. Prompt checks do not imply that a future image will render the font, text, or topology correctly; those are checked after the human returns an image.
