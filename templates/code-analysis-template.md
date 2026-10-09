# Code analysis — {{analysis_id}}

Use the user's language for this report. Replace placeholders and omit irrelevant sections. Keep structural facts consistent with the accompanying `architecture-spec.json`.

## Scope and source snapshot

- Repository label:
- Revision / local-change state / unavailable version information:
- Included directories and files:
- Entry points and active configuration:
- Excluded or unread areas:
- Requested figure scope and intended reader:

## Project motivation and intended framing

- Context status: user story / README-derived / inferred / pending / skipped.
- Source: user-provided summary and/or the target README path and relevant section.
- Motivation: whose problem the project addresses and why it exists.
- Intended reader takeaway and emphasis:
- Stated style or mood preferences, if any:
- Inferred framing, remaining assumptions, or differences between README and user intent:

Preserve the user's framing for candidate design. Verify implementation claims against code separately; this optional context is not architecture evidence.

## Implementation overview

Explain what the selected code actually implements and the architecture question the figure should answer.

## Modules and responsibilities

| Module ID | English display label | Responsibility and boundary | Inputs / outputs | Source evidence |
| --- | --- | --- | --- | --- |

## Relationships and execution paths

| Relation ID | Source → target | Type and carried meaning | Phase / condition | Evidence / inference |
| --- | --- | --- | --- | --- |

Describe the main path, branching, loops, state, external integrations, and relevant training/inference differences. Distinguish what is shared from what is separately instantiated.

## Core mechanisms and required details

Identify operations or boundaries that a faithful figure must preserve. Explain which implementation details can be grouped without changing meaning.

## Terminology

| Source term | English figure label | Meaning / disambiguation |
| --- | --- | --- |

## Uncertainties and discrepancies

| ID | Missing or conflicting information | Consequence for the figure | Evidence / resolution needed |
| --- | --- | --- | --- |

Do not claim that unread code is absent. Distinguish documented intent from implementation and explain any deliberately narrowed scope.

## Human reference and downstream use

- Facts or assumptions whose correction would change the architecture:
- Proposed architecture focus; candidate design remains a later decision:
- Foundation completeness and remaining limitations:
- Changes from the preceding analysis version, if any:
