# C2A — Code to Architecture

C2A 是一个通用 Agent SKILL：从代码项目理解架构，设计候选方案，交付英文生图 prompt 与参考素材，并在用户回传图片后审阅、修订 prompt。

**图片由人类在外部工具生成。C2A 无需生图 API，也不会调用生图工具。** 最终交付是 `architecture-prompt.md`，同时保留代码分析、候选版本、参考图和审阅记录。

## 安装

C2A 是**多文件 SKILL**：除 [SKILL.md](SKILL.md) 外，还包含 `references/`、`templates/`、`assets/`、`scripts/`，且内部互相以 SKILL.md 为基准的相对路径引用（见 [SKILL.md](SKILL.md) 的 Working boundary）。因此**必须整体安装整个项目目录，不能只复制 SKILL.md**，否则参考图检索、模板加载会静默失效。

1. 将本项目放到宿主 Agent 的技能目录下，**目录名必须为 `c2a`**（与 SKILL.md 的 `name` 字段一致）。
2. 保持内部目录结构不变。运行产物写到工作区（如 `c2a-runs/`），不要写进安装后的 SKILL。

Claude Code 示例：

```bash
# 个人级：所有项目可用
git clone https://github.com/JovinGiogic/c2a.git ~/.claude/skills/c2a
```

其他宿主：若没有原生技能机制，把本项目路径告诉 Agent，让其读取 SKILL.md 即可，无需安装步骤。

验证安装（期望输出 `PASS`）：

```bash
cd <安装位置>/c2a && python scripts/validate_artifacts.py --package .
```

说明：`assets/` 约 23 MB（1064 条参考索引、815 张 PNG 预览）。核心的代码分析与 prompt 能力**不依赖**它，仅参考图检索需要。

## 使用方式

将本项目放入所用 Agent 支持的技能目录，并使用名称 `c2a`。具体发现机制由宿主决定；没有原生技能机制时，让 Agent 读取本项目的 [SKILL.md](SKILL.md) 即可。

核心能力只要求读取/搜索代码及输出文本。可选 Python 脚本使用标准库。图片审阅需要视觉能力；没有视觉能力的 Agent 可以继续处理代码、prompt 及人类提供的观察，但不会声称已经看图。

启动示例：

```text
请使用 C2A，分析当前代码仓库，为核心架构设计两份有实际差异的候选生图 prompt。
先给出代码分析中间产物供我核对，再进行候选设计。
有适合的参考图时一并提供，并说明每份 prompt 应搭配哪些图。
```

也可以指定子目录、入口、配置、训练/推理路径或详略程度。未要求分步确认时，Agent 可根据授权连续推进到 prompt 交付；交付后由人类自行生图。

**可选的项目动机故事是最开始的一步。** 你可以在首次请求中用 2–5 句话说明项目为什么做、为谁解决什么问题、希望读者理解什么，以及期望的风格或氛围。Agent 首先轻量检查目标项目的 README：有就默认读取动机与概述；没有可读 README 且你未提供故事，就立即询问，不会先让你等待代码分析或参考图检索。可以回复“跳过”；支持异步提问的宿主可在等待时继续代码分析。你的叙述优先于 README 中的项目意图，用来指导表达重点与风格，图中的架构事实仍需代码验证。

**收到交付后，先打开 Agent 链接的 `reference-guide.md`。** 按指南打开完整 prompt、复制到生图工具、按顺序上传所列参考图，再生成图片。指南会给出当前候选/版本的实际保存目录和可复制的回传消息；没有参考图也会保留完整操作步骤。你可以将图片保存到运行目录下的 `returned-images/<候选>/<版本>/`，或在对话中上传图片并注明候选/版本，由 Agent 在可保存时归档。每次修订与最终交付都会提供相应指南；使用 `final/` 中的 prompt 生图时，仍按所选候选/版本回传。

回传示例：

```text
这是 C01/v01 对应的生成结果，已保存到 c2a-runs/my-project/returned-images/C01/v01/result-01.png（也可直接上传到对话）。
我使用了原始 prompt，未做修改；若修改过，会一并提供实际提交的文本。
请对照代码分析和该版本 prompt 审阅，保留它的模块分组，修复箭头和文字问题，输出 v02 完整 prompt。
```

最终整理示例：

```text
选择 C01/v02，请整理最终 architecture-prompt.md、参考图清单和附件，保留分析与候选历史。
```

## 流程与产物

| 阶段 | 工作 | 产物 |
| --- | --- | --- |
| S0 之前（可选） | 默认读取项目 README；没有则立即询问动机故事，可跳过 | 动机、读者理解重点与风格偏好，带入分析和候选方案 |
| S0 | 代码架构分析 | `code-analysis.md`、`architecture-spec.json` |
| S1 | 项目相关的候选设计 | `candidate-plan.md` |
| S2 | 完整 prompt 与参考图交付 | 各候选的 `architecture-prompt.md`、`reference-guide.md`、参考附件 |
| 人类生图 | 人类在外部工具生成并回传 | 带候选/版本对应关系的图片 |
| S3 | 对照代码与 prompt 审阅图片 | `review.md` 类审阅报告 |
| S4 | 修订 prompt | 新版本完整 prompt、参考图清单、修改说明 |
| S5 | 整理选定版本 | `final/architecture-prompt.md` 及配套参考图 |

S4 后可再次生图并回到 S3。只需要 prompt 时，可以直接交付，无须回传图片。

代码分析报告面向人类解释范围、源码依据、关键执行路径和不确定项；结构化规格保存模块、关系、分组和术语，供设计与审阅共同参考。候选数量按任务决定，不限制为固定轮次或固定张数。

```text
c2a-runs/<project>/
├── analysis/A01/
│   ├── code-analysis.md
│   └── architecture-spec.json
├── candidate-plan.md
├── candidates/C01/v01/
│   ├── architecture-prompt.md
│   ├── reference-guide.md
│   └── references/                 # 按需提供
├── returned-images/C01/v01/       # 交付时准备好，供保存 result-01.png 等结果
├── reviews/
├── manifest.json
└── final/
    ├── architecture-prompt.md
    ├── reference-guide.md
    └── references/                 # 按需提供
```

运行目录应放在工作区或用户指定位置，不写入安装后的 SKILL。每次修订保留原版本；分析依据变化时创建 A02 等新分析版本。

## 固定标准与设计自由度

- 生图 prompt 正文使用英文，图内文字使用英文，字体统一指定 **Comic Sans MS**。
- 每份 prompt 完整、自包含，包含架构、可见文字、连线、布局和约束。
- 每份 prompt（含候选、修订和最终版）总长度不得超过 **7000 字符**，按整个文件的 Unicode 字符计数，包含空格、换行、Markdown 与参考图指令，不按字节或 token 计数。交付前校验，字符数记录在指南中。
- 模块与关系来自代码和有效配置；文档辅助解释，不替代实现依据。
- 主题、布局、配色、画幅、密度及参考图按项目分析决定。字体选择不限定整体主题。
- 分析报告、审阅和交互可以使用中文。

## 参考素材

[素材说明](assets/README.md)与[参考索引](assets/reference-index.jsonl)包含布局/风格图板、筛选后的图标、结构示意片段及高层概念图。保留可上传的 PNG 预览及必要的源素材、来源和许可信息。

参考图只借鉴明确指定的视觉要素。Agent 将所选预览复制进候选附件目录，并在 `reference-guide.md` 中说明实际位置、附件顺序、借鉴内容与限制。prompt 中用 `Reference Image 1` 等编号关联附件；图中的事实与英文标签仍由 prompt 完整定义。未配图时也应能根据文本绘制。

检索和检查脚本均可选，使用 Python 3.10 或更新版本，无第三方运行依赖：

```bash
python scripts/find_references.py "encoder decoder skip" --limit 6
python scripts/validate_artifacts.py --package .
python scripts/validate_artifacts.py --run /path/to/run --source-root /path/to/code
python -m unittest discover -s tests -v
```

检查脚本验证结构、路径、版本对应、7000 字符上限及基础 prompt 约束；源码语义和真实图片仍需 Agent/人类审阅。字体若无法从图片可靠辨认，应记为待确认。

## 项目结构

- [SKILL.md](SKILL.md)：通用入口与阶段流程。
- `references/`：按阶段加载的分析、设计、参考图、审阅和产物规范。
- `templates/`：中间产物及交付物模板。
- `assets/`：可检索、可交付的参考素材。
- `scripts/`：可选的检索与校验工具。
- `tests/`：产物校验与参考检索的行为测试。

项目文本与代码沿用 [MIT-0 许可证](LICENSE)。保留素材的来源及许可见 [素材来源说明](assets/ATTRIBUTION.md)和各索引记录。

## 致谢

本项目由 [paper-framework-figure-studio-pro](https://github.com/c-narcissus/paper-framework-figure-studio-pro)（作者 c-narcissus，MIT-0）改造而来，沿用其参考素材，第三方图标分别来自 **Lucide**（ISC）与 **Tabler**（MIT），各自许可文本与出处见 [素材来源说明](assets/ATTRIBUTION.md)。谨向原作者的工作致以诚挚谢意。

## English

C2A is an Agent-neutral skill for understanding implemented code and preparing architecture-figure prompts. It preserves a human-readable code analysis and a structured architecture specification, proposes useful candidate approaches, and delivers complete prompts with optional reference-image attachments. The human generates images externally, returns them for review, and chooses which prompt to refine or finalize.

### Installation

C2A is a multi-file skill: besides `SKILL.md` it ships `references/`, `templates/`, `assets/`, and `scripts/`, all resolved relative to `SKILL.md`. Install the **whole directory**, not just `SKILL.md`, and name the installed directory `c2a` (matching the `name` field in `SKILL.md`). Keep the internal structure intact or reference lookup and templates break silently.

For Claude Code:

```bash
# Personal: available to all projects
git clone https://github.com/JovinGiogic/c2a.git ~/.claude/skills/c2a
# Or symlink it in place (edits apply immediately, no 23 MB copy)
ln -s /path/to/c2a ~/.claude/skills/c2a
# Project: shipped with a repository
cp -r c2a <your-repo>/.claude/skills/c2a
```

Hosts without a native skill mechanism need no install step — point the Agent at `SKILL.md`. Verify with `python scripts/validate_artifacts.py --package .` (expect `PASS`). The `assets/` reference library is ~23 MB and optional; the core code-analysis and prompt workflow does not depend on it.

Load [SKILL.md](SKILL.md) through your host's skill mechanism or ask an Agent to read it directly. File reading/search and text output are sufficient for the core workflow; visual review additionally needs image access and visual capability. The optional Python 3.10+ utilities use only the standard library.

Prompts and visible figure text are English. Every prompt requires **Comic Sans MS** for all visible text and must contain **at most 7000 Unicode characters**, including whitespace, Markdown, and reference instructions in the complete file. This applies to every candidate, revision, and final copy; the validator enforces the limit. Theme, layout, palette, aspect ratio, and detail follow the particular project and its intended framing. Each prompt fully specifies architecture and labels; reference images supplement appearance and do not introduce unsupported facts. Analysis and conversation can use the user's language.

Start with a repository, relevant scope/entry/configuration, and any design preferences. Before S0, optionally provide a short project motivation story: why it exists, whose problem it addresses, the reader takeaway, and desired mood. The Agent first checks the target README and reads its motivation and overview by default. If no readable README or supplied story is available, it asks immediately, before deeper code analysis or reference retrieval; you may skip. Hosts with nonblocking questions can continue code analysis while you answer. User framing takes precedence over README-derived intent and informs visual style, while code remains the basis for architecture facts.

Outputs then follow S0 code foundation → S1 candidate design → S2 prompt delivery → human generation → S3 image review → S4 prompt revision → S5 final handoff. **Open the linked `reference-guide.md` first** at every delivery: it explains which complete prompt to copy, which images to attach and in what order, where to save results, and how to request review. Return images to the run's `returned-images/<candidate>/<version>/` directory, or upload them in the conversation with the candidate/version for the Agent to archive when supported. The guide includes the actual location and a ready-to-copy return message. A final prompt still maps to the selected candidate/version. Repeat the human-generation/review loop as useful; prompt-only delivery is also supported.

The final `architecture-prompt.md` is accompanied by a reference guide and selected attachments where applicable. Analysis, candidate versions, returned images, and reviews remain available in the run directory. C2A neither calls image-generation APIs nor needs their credentials.

### Acknowledgements

This project is a modification of [paper-framework-figure-studio-pro](https://github.com/c-narcissus/paper-framework-figure-studio-pro) (authored by c-narcissus, MIT-0) and retains its reference materials. Third-party icons are sourced from **Lucide** (ISC) and **Tabler** (MIT), with their respective license texts and sources available in the [Attribution Notice](assets/ATTRIBUTION.md). We extend our sincere gratitude to the original author for their work.
