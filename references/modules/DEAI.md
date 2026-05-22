# De-AI Module Reference

Purpose: Detect and reduce AI-generated writing traces in Chinese doctoral theses.

## Core Principles

1. **Syntax preservation**: Never modify `[@key]` citations, `$...$` math, or Markdown structure
2. **Zero fabrication**: Never add data, metrics, comparisons, or claims
3. **Information density**: Every sentence must convey verifiable information
4. **Restrained wording**: Avoid unsupported certainty; use appropriate hedging

## Detection Categories

### Pattern-Based Detection (9 categories)

| Category | Pattern Count | Example |
|----------|--------------|---------|
| empty_phrase | 8 | "显著提升" → replace with "MAE 降低 12%" |
| over_confident | 10 | "显而易见", "必然" → "实验结果表明" |
| vague_quantifier | 9 | "大量研究" → "三项研究 [1-3]" |
| template_expr | 7 | "近年来", "随着科技的飞速发展" |
| filler_connector | 8 | "总之", "值得注意的是" → 删除 |
| **exaggerated_significance** | 8 | "至关重要的作用", "里程碑意义" → 说具体贡献 |
| **promotional_language** | 7 | "卓有成效", "大放异彩" → 用数据说话 |
| **vague_attribution** | 6 | "专家认为", "研究表明" → 具体引用 |
| **formulaic_structure** | 4 | "不仅…而且…更…", "一方面…另一方面" |

### Structure-Based Detection (7 checks)

| Check | Code | Description |
|-------|------|-------------|
| C1 | Pattern scan | Keyword-level AI trace detection |
| C2 | parallel_structure | 3+ consecutive lines sharing same opening |
| C3 | low_information_density | Boilerplate-heavy, evidence-light paragraphs |
| **C4** | **conclusion_first** | **先下结论再补证据 — 博士论文大忌** |
| **C5** | **word_repetition** | **段内同一词语出现 3+ 次** |
| **C6** | **tautology** | **同义反复：如"研究和探索"、"分析与讨论"** |
| **C7** | **sentence_monotony** | **连续 4+ 句字数相近，节奏单调** |

## Quick Start

```bash
# Full document analysis
uv run python deai_check.py thesis.md --analyze

# Check specific section
uv run python deai_check.py thesis.md --section introduction

# Generate JSON fix suggestions
uv run python deai_check.py thesis.md --fix-suggestions
```

## AI Density Scoring

| Score | Action |
|-------|--------|
| >70% | Urgent: immediate rewrite |
| 50-70% | High: rewrite soon |
| 30-50% | Medium: review and revise |
| <30% | Low: light polish only |

## Key Principle: 先研究问题，再提对策

博士论文的表述逻辑是：
1. 提出问题 → 2. 分析数据/实验 → 3. 推导结论

AI 则习惯：
1. ~~先下结论~~ → 2. ~~补充证据~~ → 3. ~~重复结论~~→ 4. ~~尽力辩解~~ → 5. ~~大量括号解释~~

> Full details: see [`../DEAI_GUIDE.md`](../DEAI_GUIDE.md)
> Pattern inspiration: [Humanizer-zh](../../Humanizer-zh/SKILL.md), [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
