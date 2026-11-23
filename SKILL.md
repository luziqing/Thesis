---
name: thesis-zh
description: Chinese Markdown thesis assistant for multi-file .md degree thesis projects (Pandoc). Use this skill whenever a user works on a Chinese doctoral thesis in Markdown format needing topic/开题 evaluation, literature survey and review synthesis, structure mapping, GB/T 7714 bibliography checks, citation authenticity verification, terminology consistency, logic coherence review, heading lead-in checks, title optimization, faithful-language polishing (tone calibration, Chinese-to-English abstract), de-AI editing, experiment chapter review, pre-submission review with severity gating, or Pandoc export. Trigger even for single issues like "评估选题", "帮我做文献调研", "检查论文结构", "检查国标格式", "看看绪论逻辑", "润色这一段", "送审前审一遍", "毕业论文", "学位论文", "博士论文", or "检查 Markdown 论文"; also covers claim-evidence, gap specificity, ablation alignment, figure planning.
metadata:
  category: academic-writing
  tags: [markdown, thesis, chinese, phd, pandoc, gb7714, topic, survey, citation, structure, bibliography, deai, polish, logic, review]
argument-hint: "[thesis.md 或 thesis_dir/] [--section SECTION] [--module MODULE]"
allowed-tools: Read, Glob, Grep, Bash(uv *), Bash(python *), Bash(pandoc *)
---

# Markdown 中文学位论文助手

处理已有中文 Markdown 学位论文项目的定向问题：先判断最小匹配模块，再运行对应脚本，最后以审阅友好格式返回问题和建议。

## Triggering

当用户拥有一个现有中文 `.md` 学位论文项目，并希望你处理以下任务时使用本 skill：选题论证与开题评估；文献调研与综述章研究现状梳理；Pandoc 导出或工具链排查；学位论文格式、国标、学校规范检查；术语与缩略语一致性；引用真实性核验；逻辑连贯性、文献综述质量、标题后导语、跨章节闭合；标题优化、忠于原意的润色、语气校准、学术表达、去 AI 化；实验章节语言与结构审阅；送审/答辩前统一核查。

即使用户只提到单一问题，例如"评估这个选题""帮我做文献调研""检查绪论逻辑""按 GB/T 7714 看参考文献""润色这一段""送审前审一遍"或"帮我把论文导出为 PDF"，也应触发本 skill。

`topic` / `survey` 属论文开工前后的调研阶段，虽不要求先有稿件，但仍服务于学位论文工程，故纳入本 skill；对英文会议/期刊论文的同类需求仍转对应 skill。

## Do Not Use

不要将此 skill 用于：

- 英文会议或期刊论文（编辑用 `latex-paper-en`）
- LaTeX `.tex` 项目（使用 `latex-thesis-zh`）
- Typst 项目
- 仅有 DOCX/PDF、没有 Markdown 源文件的场景
- 与学位论文无关的纯文献调研（本 skill 的 `survey` 服务于论文综述章；通用调研不属于此）
- 从零写一篇学位论文（`topic` 只做选题评估，`survey` 只做调研综合，均不起草正文）
- 英文期刊投稿门控检查（使用 `paper-audit`；本 skill 的 `review` 只面向中文学位论文送审/答辩）
- 规避 AI 使用检测或规避查重（见 Chinese Writing Boundaries 反模式黑名单）

## Module Router

| Module | Use when | Primary command | Read next |
| --- | --- | --- | --- |
| `topic` | 选题论证、开题评估、在多个候选选题间做取舍 | LLM 判断（无脚本），流程见参考 | `references/modules/TOPIC.md` |
| `survey` | 文献调研、写/重构综述章前的研究现状梳理 | LLM 判断 + 检索/子代理，流程见参考 | `references/modules/SURVEY.md` |
| `export` | Need to export Markdown thesis to PDF/DOCX via Pandoc | `uv run python $SKILL_DIR/scripts/export.py thesis_dir/` | `references/modules/EXPORT.md` |
| `format` | User asks about typos, punctuation, or formatting | `uv run python $SKILL_DIR/scripts/check_format.py thesis.md --strict` | `references/modules/FORMAT.md` |
| `structure` | Need chapter/section map or thesis skeleton overview | `uv run python $SKILL_DIR/scripts/map_structure.py thesis_dir/` | `references/STRUCTURE_GUIDE.md` |
| `consistency` | Terms, abbreviations, or naming drift across chapters | `uv run python $SKILL_DIR/scripts/check_consistency.py thesis_dir/ --terms` | `references/modules/CONSISTENCY.md` |
| `bibliography` | GB/T 7714 or BibTeX validation | `uv run python $SKILL_DIR/scripts/verify_bib.py references.bib --standard gb7714` | `references/modules/BIBLIOGRAPHY.md` |
| `title` | Optimize Chinese thesis titles and chapter titles | `uv run python $SKILL_DIR/scripts/optimize_title.py thesis.md --check` | `references/modules/TITLE.md` |
| `deai` | Reduce AI-writing traces in visible Chinese prose | `uv run python $SKILL_DIR/scripts/deai_check.py thesis.md --analyze` | `references/modules/DEAI.md` |
| `polish` | 忠于原意的语言润色、语气校准、按节惯例、英文摘要中译英 | LLM 改写（受 Chinese Writing Boundaries 约束），流程见参考 | `references/modules/POLISH.md` + CONTENT_RULES |
| `logic` | Check logical coherence, introduction funnel, heading lead-ins, lit review quality, chapter mainline, and cross-section closure | `uv run python $SKILL_DIR/scripts/analyze_logic.py thesis.md --section related` | `references/modules/LOGIC.md` + CONTENT_RULES |
| `experiment` | Review experiment chapter language, discussion layering, and conclusion completeness | `uv run python $SKILL_DIR/scripts/analyze_experiment.py thesis.md --section experiments` | `references/modules/EXPERIMENT.md` + CONTENT_RULES |
| `review` | 送审/答辩前统一核查、严重度分级与送审裁决 | 编排已有脚本 + LLM 判断，流程见参考 | `references/modules/REVIEW.md` + CONTENT_RULES |

## Required Inputs

- 论文入口文件（如 `thesis.md`）或论文目录（如 `thesis_dir/`，包含多个 `.md` 文件）——`export`/`format`/`structure`/`consistency`/`bibliography`/`title`/`deai`/`logic`/`experiment`/`polish`/`review` 需要。
- `topic`/`survey` 不需要稿件：需要选题描述 / 课题或 RQ，可附能力自述、候选选题、检索能力说明。
- 可选 `--section SECTION`，当用户只关注某一章或某一节。
- 可选 bibliography 路径（`.bib` 文件）与学校上下文（如燕山大学）。

如果参数不完整，只追问入口 `.md` 文件（或目录，或选题/课题描述）和目标模块，不额外扩展问题。

## Output Contract

- 使用审阅友好的格式返回问题：`<!-- MODULE (L##) [Severity] [Priority]: ... -->`
- 明确给出执行的命令；若脚本失败，必须报告退出码和关键 stderr。
- 将"检查结果"和"建议改写"分开陈述，避免把脚本诊断和正文润色混在一起。
- 默认保留 `[@key]` 引用、`$...$` / `$$...$$` 数学公式、`[^footnote]` 脚注和图片引用。
- 改写类交付固定三块：`检查结果` / `改写稿` / `改动说明（含未改及原因）`。

## Workflow

1. Parse `$ARGUMENTS` for entry file/directory and module. If missing, ask for the thesis `.md` entry file (or directory) and target module.
2. Read the one file in the "Read next" column for that module. For any rewrite task, also apply the **Chinese Writing Boundaries** section below.
2b. 审阅/改写模块另读 `references/CONTENT_RULES.md`，只作审阅线索。
3. **Script-driven modules** (`export`/`format`/`structure`/`consistency`/`bibliography`/`title`/`deai`/`logic`/`experiment`): run the command exactly as given in the Module Router. If `uv` is unavailable, substitute `python` and report the substitution; never mix the two forms within one run. **Judgment-driven modules** (`topic`/`survey`/`polish`/`review`): no script; follow the referenced guide's procedure and capability preconditions (e.g. `survey` requires retrieval; `review` orchestrates existing scripts + LLM judgment). Do not fabricate a command or a script result for these.
4. Return findings as `<!-- Module (L##) [Severity] [Priority]: ... -->`. Report exact command and exit code on failure. For judgment-driven modules, still tag findings with severity and cite the specific evidence/rule.
5. For multi-file thesis, the scripts will automatically scan the directory for all `.md` files.
6. Before delivering rewritten prose, run the Quick Checks in Chinese Writing Boundaries. Any failure returns to the audit step. `polish` rewrites are additionally bound by that section as the single source of truth.
7. Citation authenticity: whenever `survey`/`review`/`bibliography` relies on retrieved references, apply `references/CITATION_VERIFICATION.md`; never present a memory-sourced reference as verified.

> **Windows**：脚本已内置 `sys.stdout.reconfigure(encoding='utf-8')` 保护，无需设 `PYTHONIOENCODING`。

## Chinese Writing Boundaries（中文写作边界 · 改写类模块共用）

> **唯一真源**：本节界定「能改 / 禁改 / 改到什么程度算过头」。`references/` 内任何指南与本节冲突时**以本节为准**；`scripts/deai_check.py` 只产出线索，**命中 ≠ 改写判据**。细则见 `references/DEAI_GUIDE.md` §写作保护边界。

**优先级**：① 事实保真（数字、单位、限定语、`[@key]`、`$...$`、术语、定义逐字保留）→ ② 学位论文语域 → ③ 用户要求与学校模板 → ④ 结构与信息密度 → ⑤ 套话、句式、标点。

**🔴 禁改清单（禁止过度纠正）**
- 证据绑定的 hedging：`可能` `倾向于` `提示` `在…条件下`。动词阶梯 `证明/证实 > 表明/验证 > 提示/可能`，**只允许下调、禁止上调**（❌ `结果提示`→`结果证明`）。
- 带数字或 p 值的程度词：`显著降低 12%`、`显著优于基线(p<0.01)`。有证据即非空话，脚本已豁免（❌ 删掉 `显著 (p<0.01)`）。
- 被动语态（施动者无关）、`本文/本研究`、定义/术语/符号/数据集名。不轮换同义词，不把 `本文` 改成 `我/我们`。
- `[@key]`、`$...$`/`$$...$$`、`[^n]`、图表与交叉引用。保护 **Pandoc 语法**，不是 `\cite{}` / `\begin{equation}`。
- 绪论的研究意义句、结论章功能性总结。`综上所述` `不仅…而且` `显著` `大量` 按语境判定，有证据或承担章节功能时保留，**禁止批量替换**。

**证据纪律**：每个实证断言自问「有无数字/图表/引用支撑」「动词强度 ≤ 证据强度」。无证据 → 补指针；补不到 → 标 `【待补证】`，不得删掉了事、不得编数字。模糊量级 → 归属到方法/指标/基线的区间（`相比最强基线在 3 个数据集上提升 2–6%`）；先比最强基线。

**反模式黑名单（不要做）**：拔高/弱化结论强度、删 hedging；注入口语/幽默/第一人称「个性」；为规避 AI 使用检测而增删事实、改引用、注水（本 skill **不用于规避检测**，AI 辅助须按学校/投稿政策披露）；只看脚本命中批量替换；重排句序、改引用键或公式；改写正文夹带脚本诊断。命中即拒绝该改动并在改动说明写明原因。

**交付前 Quick Checks**（任一不过 → 回审计步）：① 数字/单位/p 值/`[@key]`/`$...$` 逐字一致；② hedging 未升格、断言未超证据；③ 无新增数据/贡献/引用，未核处标 `【待补证】`；④ 段落数与论点覆盖不变；⑤ 无破折号堆砌、三项凑数排比、加粗开头列表、Unicode 箭头；⑥ 三块交付（`检查结果`/`改写稿`/`改动说明`）。5 维验收（细则见 `DEAI_GUIDE.md`）各 1–10 分，**合计 <35 退回重写**。

**改写流程**：1. **审计（先不改）** 跑脚本取线索 → 按禁改清单排除误报 → 列「必改 / 语境待定 / 不改及原因」三栏；2. 🔴 CHECKPOINT · 🛑 STOP 涉及结论强度、研究意义、术语或引用的改动，先列清单等用户确认，不直接落盘；3. **改写** 同结构同内容，只删 tells、只下调动词；4. **报告** 说明含「未命中但不改」项及原因，复跑脚本密度不得高于改前。

**失败模式**
- 若只给内联文本、无入口 `.md` → 追问入口；须直接交付则转人工清单并标 `dry_run`；仍失败 → 声明「脚本未运行」，不伪报结果。
- 若脚本报错 / 退出码非 0 → 报告退出码 + 关键 stderr 并转人工清单；仍失败 → 按 `DEAI_GUIDE.md` 检测清单逐条核对。
- 若脚本密度触发重写但人工判合格 → 按禁改清单复核并记录冲突；仍失败 → 输出「脚本↔边界冲突」交用户裁决。

## Content Rules（内容层规则 · 审阅/改写模块共用）

> 与 Chinese Writing Boundaries 并列：事实与形式改写以该节为唯一真源；本节只管主张-证据、论证链与图表承载。细则见 `references/CONTENT_RULES.md`。

- **主张-证据**：每条实证主张配证据与最强许可措辞；头条数字 1–2 个；同一主张只出现一次，各处强度一致。
- **缺口与组件**：具体肯定前人 → 失效条件与原因 → 对问题的观察 → 方法；组件按「需要 → 机制 → 性质」写关系，不并列罗列。
- **消融与图表**：消融与主张一一对应，无证据软化或标 `【待补证】`；先出图表规划表，一图一主张，结果图留白不编造。
- **边界**：统计口径只作线索，不向均值磨平；推文营销模板与 CVPR/LaTeX 专属规则不进正文（§7）。

## Safety Boundaries

- Never fabricate citations, funding statements, acknowledgements, or academic claims.
- Never rewrite `[@key]` citations, `$...$` math blocks, footnotes, or bibliography keys unless explicitly asked.
- Treat title suggestions, de-AI revisions, and logic comments as proposals; keep source-preserving checks separate from edits.
- Any rewrite of visible prose is additionally bound by **Chinese Writing Boundaries** above; when the two conflict, that section wins.

## Reference Map

- `references/TOPIC_EVALUATION.md`: 选题评估——五维框架、致命缺陷审计、学制/能力匹配、范式探测、可行性、三档裁决.
- `references/SURVEY_GUIDE.md`: 文献调研与综述综合——冻结 RQ、多视角检索、MECE 综合、自对抗、六道门、hedge 阶梯.
- `references/CITATION_VERIFICATION.md`: 引用真实性核验——能力阶梯、五状态分级、独立核验与收敛规则（survey/review/bibliography 共用）.
- `references/POLISH_GUIDE.md`: 忠于原意的润色——轻触默认、分节惯例、动词阶梯/phrasebank、中译英；服从 Chinese Writing Boundaries.
- `references/REVIEW_GUIDE.md`: 送审前统一核查——五维审查、CRITICAL/MAJOR/MINOR、完整性门控、禁词扫描、评分裁决.
- `references/EXPORT_GUIDE.md`: Pandoc export strategy and troubleshooting.
- `references/GB_STANDARD.md`: GB/T 7714 and bibliography-related checks.
- `references/STRUCTURE_GUIDE.md`: thesis structure expectations and chapter mapping.
- `references/LOGIC_COHERENCE.md`: logic, coherence, heading lead-ins, consistency, and literature-review expectations.
- `references/TITLE_OPTIMIZATION.md`: Chinese academic title heuristics.
- `references/DEAI_GUIDE.md`: de-AI heuristics **and §写作保护边界（细则、反例对照、验收表）**.
- `references/ACADEMIC_STYLE_ZH.md` / `WRITING_PHILOSOPHY_ZH.md`: 通用中文学术用词与叙事原则；去 AI 化时须服从本节优先级。
- `references/FORBIDDEN_TERMS.md`: 受保护术语；LaTeX 命令示例仅在 `.tex` 项目适用，Markdown 项目以 `[@key]` / `$...$` 为准。
- `references/TECH_DOC_STYLE_ZH.md`: 中文科技文档排版，适用于学位论文**之外**的文体。
- `references/modules/EXPERIMENT.md`: experiment-chapter review criteria.
- `references/modules/TOPIC.md` / `SURVEY.md` / `POLISH.md` / `REVIEW.md`: router-facing summaries for the judgment-driven modules.
- `references/modules/PRECHECK.md`: 盲审前逐章自查清单（P0/P1/P2），与 `review` 模块协同.
- `references/UNIVERSITIES/`: school-specific constraints (e.g., `yanshan.md`).
- `COMPARISON-supervisor-skills.md`: 与 Supervisor-Skills 写作能力的对照、缺口判定与补充落点记录.
- `references/CONTENT_RULES.md`: 内容层规则（主张-证据、缺口、组件关系、消融、图表规划、不可迁移清单）.
- `COMPARISON-bestpaper-writing.md`: 与 Best-Paper-Writing-Skill 的规则对照、可迁移判定与落点.

每次只读取 Module Router 的 "Read next" 列 + 本节 Chinese Writing Boundaries；不加载其它模块指南。改写类（`polish`/`deai`）额外遵循 Chinese Writing Boundaries 为唯一真源。

## Example Requests

- "我有两个候选选题，帮我评估哪个值得做博士论文。"（`topic`）
- "围绕这个方向帮我做一次文献调研，梳理研究现状和空白。"（`survey`）
- "把这段讨论润色一下，语气别太肯定；引用和公式别动。"（`polish`）
- "送审前帮我把全文审一遍，按严重程度列问题。"（`review`）
- "帮我把这个 Markdown 学位论文目录导出为 PDF，检查 Pandoc 配置是否正确。"
- "请梳理这篇博士论文的章节结构，并检查术语和缩略语是否前后统一。"
- "按 GB/T 7714 帮我检查参考文献，再看看绪论是不是有明显 AI 腔。"
- "检查 related work 的逻辑链条和研究空白推导，但不要动任何引用和公式。"
- "检查绪论里每个主张有没有证据支撑，实验章的消融和结论对不对得上。"（`logic` + `experiment` + CONTENT_RULES）
- "检查各章、各节、四级标题后有没有先写导语。"
