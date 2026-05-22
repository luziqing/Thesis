---
name: thesis-zh
description: Chinese Markdown thesis assistant for multi-file .md degree thesis projects (Pandoc). Use this skill whenever a user works on a Chinese doctoral thesis in Markdown format needing structure mapping, GB/T 7714 bibliography checks, terminology consistency, logic coherence review, heading lead-in checks, title optimization, de-AI editing, experiment chapter review, or Pandoc export. Trigger even for single issues like "检查论文结构", "检查国标格式", "看看绪论逻辑", "毕业论文", "学位论文", "博士论文", or "检查 Markdown 论文".
metadata:
  category: academic-writing
  tags: [markdown, thesis, chinese, phd, pandoc, gb7714, structure, bibliography, deai, logic]
argument-hint: "[thesis.md 或 thesis_dir/] [--section SECTION] [--module MODULE]"
allowed-tools: Read, Glob, Grep, Bash(uv *), Bash(python *), Bash(pandoc *)
---

# Markdown 中文学位论文助手

使用此 skill 处理已有中文 Markdown 学位论文项目中的定向问题。保持低摩擦：先判断最小匹配模块，再运行对应脚本，最后以论文审阅友好的格式返回问题和建议。

## Capability Summary

- 将 Markdown 论文通过 Pandoc 导出为 PDF / DOCX。
- 检查论文格式、GB/T 7714 相关要求、章节结构和术语一致性。
- 审阅逻辑连贯性、文献综述质量、章节/小节/四级标题导语完整性、实验章节写法、标题表达与 AI 痕迹。
- 在不破坏 Pandoc 引用 `[@key]`、数学公式 `$...$` / `$$...$$`、脚注和交叉引用的前提下给出可落地的中文论文修改建议。

## Triggering

当用户拥有一个现有中文 `.md` 学位论文项目，并希望你帮助处理以下任务时使用本 skill：

- Pandoc 导出失败或工具链不确定
- 学位论文格式、国标或学校规范检查
- 章节结构梳理（多文件目录扫描）
- 术语、缩略语、命名一致性检查
- 逻辑连贯性、文献综述质量、标题后导语完整性、跨章节闭合检查
- 标题优化、学术表达或去 AI 化检查
- 实验章节语言与结构审阅

即使用户只提到单一问题，例如"检查绪论逻辑""按 GB/T 7714 看参考文献"或"帮我把论文导出为 PDF"，也应触发本 skill。

## Do Not Use

不要将此 skill 用于：

- 英文会议或期刊论文
- LaTeX `.tex` 项目（使用 `latex-thesis-zh`）
- Typst 项目
- 仅有 DOCX/PDF、没有 Markdown 源文件的场景
- 纯文献调研、没有学位论文工程的任务
- 从零写一篇学位论文
- 多维度审稿、评分或投稿门控检查（使用 `paper-audit`）
- 英文会议/期刊论文编辑（使用 `latex-paper-en`）

## Module Router

| Module | Use when | Primary command | Read next |
| --- | --- | --- | --- |
| `export` | Need to export Markdown thesis to PDF/DOCX via Pandoc | `uv run python $SKILL_DIR/scripts/export.py thesis_dir/` | `references/modules/EXPORT.md` |
| `format` | User asks about typos, punctuation, or formatting | `uv run python $SKILL_DIR/scripts/check_format.py thesis.md --strict` | `references/modules/FORMAT.md` |
| `structure` | Need chapter/section map or thesis skeleton overview | `uv run python $SKILL_DIR/scripts/map_structure.py thesis_dir/` | `references/STRUCTURE_GUIDE.md` |
| `consistency` | Terms, abbreviations, or naming drift across chapters | `uv run python $SKILL_DIR/scripts/check_consistency.py thesis_dir/ --terms` | `references/modules/CONSISTENCY.md` |
| `bibliography` | GB/T 7714 or BibTeX validation | `uv run python $SKILL_DIR/scripts/verify_bib.py references.bib --standard gb7714` | `references/modules/BIBLIOGRAPHY.md` |
| `title` | Optimize Chinese thesis titles and chapter titles | `uv run python $SKILL_DIR/scripts/optimize_title.py thesis.md --check` | `references/modules/TITLE.md` |
| `deai` | Reduce AI-writing traces in visible Chinese prose | `python $SKILL_DIR/scripts/deai_check.py thesis.md` | `references/modules/DEAI.md` |
| `logic` | Check logical coherence, introduction funnel, heading lead-ins, lit review quality, chapter mainline, and cross-section closure | `uv run python $SKILL_DIR/scripts/analyze_logic.py thesis.md --section related` | `references/modules/LOGIC.md` |
| `experiment` | Review experiment chapter language, discussion layering, and conclusion completeness | `uv run python $SKILL_DIR/scripts/analyze_experiment.py thesis.md --section experiments` | `references/modules/EXPERIMENT.md` |

## Required Inputs

- 论文入口文件（如 `thesis.md`）或论文目录（如 `thesis_dir/`，包含多个 `.md` 文件）。
- 可选 `--section SECTION`，当用户只关注某一章或某一节。
- 可选 bibliography 路径（`.bib` 文件），当任务聚焦参考文献。
- 可选学校上下文，当用户关心特定高校格式要求（如燕山大学）。

如果参数不完整，只追问入口 `.md` 文件（或目录）和目标模块，不额外扩展问题。

## Output Contract

- 使用审阅友好的格式返回问题：`<!-- MODULE (L##) [Severity] [Priority]: ... -->`
- 明确给出执行的命令；若脚本失败，必须报告退出码和关键 stderr。
- 将"检查结果"和"建议改写"分开陈述，避免把脚本诊断和正文润色混在一起。
- 默认保留 `[@key]` 引用、`$...$` / `$$...$$` 数学公式、`[^footnote]` 脚注和图片引用。

## Workflow

1. Parse `$ARGUMENTS` for entry file/directory and module. If missing, ask for the thesis `.md` entry file (or directory) and target module.
2. Read the one reference file tied to that module (see "Read next" column).
3. Run the corresponding script. Prefer `python $SKILL_DIR/scripts/...`; fall back to `uv run python ...` if a venv is required.
4. Return findings as `<!-- Module (L##) [Severity] [Priority]: ... -->`. Report exact command and exit code on failure.
5. For multi-file thesis, the scripts will automatically scan the directory for all `.md` files.

> **Windows 兼容性**：所有脚本已内置 `sys.stdout.reconfigure(encoding='utf-8')` 保护，无需手动设置 `PYTHONIOENCODING`。

## Safety Boundaries

- Never fabricate citations, funding statements, acknowledgements, or academic claims.
- Never rewrite `[@key]` citations, `$...$` math blocks, footnotes, or bibliography keys unless explicitly asked.
- Treat title suggestions, de-AI revisions, and logic comments as proposals; keep source-preserving checks separate from edits.

## Reference Map

- `references/EXPORT_GUIDE.md`: Pandoc export strategy and troubleshooting.
- `references/GB_STANDARD.md`: GB/T 7714 and bibliography-related checks.
- `references/STRUCTURE_GUIDE.md`: thesis structure expectations and chapter mapping.
- `references/LOGIC_COHERENCE.md`: logic, coherence, heading lead-ins, consistency, and literature-review expectations.
- `references/TITLE_OPTIMIZATION.md`: Chinese academic title heuristics.
- `references/DEAI_GUIDE.md`: de-AI review heuristics.
- `references/modules/EXPERIMENT.md`: experiment-chapter review criteria.
- `references/UNIVERSITIES/`: school-specific constraints (e.g., `yanshan.md`).

只读取当前模块所需的参考文件，避免一次加载整套指南。

## Example Requests

- "帮我把这个 Markdown 学位论文目录导出为 PDF，检查 Pandoc 配置是否正确。"
- "请梳理这篇博士论文的章节结构，并检查术语和缩略语是否前后统一。"
- "按 GB/T 7714 帮我检查参考文献，再看看绪论是不是有明显 AI 腔。"
- "检查 related work 的逻辑链条和研究空白推导，但不要动任何引用和公式。"
- "帮我检查每一章、每一节、四级标题后有没有先写导语，不要只看格式。"
