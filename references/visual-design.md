# Project-specific visual design

## Choose the question before the surface

Start from the recorded user story or README-derived motivation and use the code foundation to choose what a reader should understand: component responsibilities, an execution path, a state transition, a model mechanism, a deployment boundary, or a combination with a clear primary view. Emphasize what matters in this project rather than assuming every project is a linear data pipeline.

Translate the intended takeaway and any stated mood into concrete design choices: emphasis, reading order, grouping, theme, palette, and detail. Explain the connection in each candidate's rationale. User framing takes precedence over README-derived intent; label your own style inferences when no preference was supplied. A story may guide presentation but cannot introduce unsupported modules, mechanisms, or claims.

Use [the candidate plan template](../templates/candidate-plan-template.md). Each candidate states its reader question, architecture coverage, abstraction, visual approach, and why it is useful. Two or three distinct candidates are often enough; follow the requested count or explain why fewer meaningful alternatives exist. Do not fill a quota with color-only variations.

| Architecture characteristic | Possible visual approach | What to check |
| --- | --- | --- |
| Ordered transformations | Pipeline with grouped stages | Preserve actual branching, feedback, and state access. |
| Abstraction layers | Layered component view | Distinguish dependency from runtime flow. |
| Coordinator with tools/workers | Central coordinator or role lanes | Show the true dispatch and return paths, not an invented all-to-all mesh. |
| Training and inference | Shared core with separate phase paths | Identify shared parameters and training-only operations from code. |
| Iteration or recurrent state | Loop with an explicit condition/state boundary | Do not invent termination or feedback semantics. |
| Critical local mechanism | Overview plus a focused detail panel | The parent overview and detail panel must not duplicate a full workflow. |
| Distributed services | Deployment/ownership groups with typed connectors | A package boundary alone does not establish a process or host boundary. |

These are choices, not required layouts. A reference image can suggest visual organization, but the target structure still comes from code.

## Fixed typography, variable treatment

Every candidate uses English visible text and Comic Sans MS. Choose the other properties for the project: background, shape language, palette, accents, aspect ratio, connector treatment, detail, and density. Do not import a reference image's font. Do not assume Comic Sans MS requires a sketch or cartoon theme.

Explain color semantics, if any. Use contrast, shape, position, or line style as additional cues when color encodes meaning. Keep a symbol, color, or line style consistent within the figure; avoid a legend that gives one token conflicting meanings.

## Preserve structure while controlling detail

- Give each visible module a short English label and a clear responsibility. Show internal operations when they explain a core mechanism; generic helper modules can remain simple.
- Use connector labels or ports for carried data and scalar values when appropriate. Persistent stores, queues, external systems, and important artifacts can be first-class objects.
- Specify the true endpoints, direction, and meaning of every visible connector. Route around labels and modules; geometric convenience is not evidence of a transfer.
- Bundle genuinely equivalent connectors where that preserves meaning. Keep distinct roles distinguishable; do not impose one arrow per module pair when the code has different relations.
- Compress repeated roles with shared structure only when they really share implementation/behavior. Preserve real parallel instances or meaningful branch differences.
- Balance the canvas around the main architecture. Allocate context, legends, and detail panels according to their explanatory value. There is no universal module count, whitespace percentage, palette, or aspect ratio.
- A detail panel expands its parent; it does not add unsupported operations. Do not hide required architecture exclusively in an external caption.

## Candidate comparison

Explain each candidate's strength and tradeoff using the reader question and code coverage. Record selected reference roles and the source-analysis ID. Keep user preferences explicit, including which aspects should carry into the next version. If a preferred visual contradicts the code, preserve its useful appearance while correcting the unsupported architecture.
