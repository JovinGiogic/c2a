# Image generation and return guide

Write this guide in the user's language. Replace authoring instructions with concrete values and working links, then remove these notes before delivery. The human should be able to complete generation and return by following this file alone.

- Candidate / version:
- Analysis ID:
- Complete prompt: replace with a relative Markdown link to `architecture-prompt.md`.
- Prompt length: measured character count / 7000.
- Run directory: actual current workspace path.
- Save generated images here: actual full path to `returned-images/<candidate>/<version>/` under the run directory, plus a relative Markdown link to that prepared directory when available.
- Review state: prompt checked / image reviewed directly / human observations only / no returned image.

## Generate your image

1. Open the complete prompt linked above and copy its entire contents into your external image-generation tool. This guide explains the process; submit the prompt file's text as the image instructions.
2. Attach the reference images listed below in the indicated order. If none are listed, submit the text alone. If your tool accepts text only, the complete prompt also works without attachments.
3. Generate the image. The prompt's architecture, English labels, and Comic Sans MS requirement take priority over reference appearance. Keep the original prompt for comparison; if you edit it in the tool, retain the actual submitted text and include it when returning the image.

## Attachments in order

| ID in manifest / prompt | Actual image file | Origin / asset ID | Borrow | Avoid | Visual inspection |
| --- | --- | --- | --- | --- | --- |

Replace file cells with actual relative Markdown links. `R1` maps to `Reference Image 1`, and so on. Copy the files into this package's `references/` directory. If there are no references, replace this table with “No reference images are required; use the complete text prompt.”

## Save and return your result

1. Download the generated image and save it in the **Save generated images here** directory above. Use distinct names such as `result-01.png`, `result-02.png`, keeping the actual image format/extension and preserving previous results. Save results in the return directory; the `references/` files are visual inputs.
2. If you cannot save to that workspace, upload the image in this conversation or provide an accessible file path, together with the candidate/version. The Agent will copy accessible originals into the return directory and tell you the saved path, or explain if this host cannot archive uploads.
3. Send a message using the example below. Include the candidate/version even if you used `final/architecture-prompt.md`. If you changed the prompt before generation, include the actual submitted text or its accessible file path. Optionally say what to preserve and what to improve.

Replace candidate/version and the image location in this example with the real values before delivering the guide. Translate it into the user's language and keep it ready to copy:

```text
This is the generated result for {{candidate_id}}/{{version_id}}.
The image is saved at {{actual_return_directory}}/result-01.png (or attached here).
I used the original prompt without edits.
Please review it against the code analysis and this prompt version, then provide a complete revised prompt if needed.
```

The Agent will confirm which version and image it is reviewing, report concrete issues, and provide a new complete prompt and guide when refinement is needed. Follow the new version's guide for the next generation and return. If you only need the prompt, you may stop without generating an image.

## Sources

Record the selected materials' source and license information or provenance links, including whether a reference came from a previous returned candidate. Do not list an unavailable historical source image as an attachment.
