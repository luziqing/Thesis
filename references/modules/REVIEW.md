# Review Module Reference — 送审/答辩前统一核查

Purpose: 在送盲审/答辩前给出带严重度分级的优先级问题清单与送审裁决（不是改写）。

> 🔴 **边界**：面向中文学位论文送审/答辩前；英文期刊投稿门控用 `paper-audit`。与 `PRECHECK.md`（逐章自查清单）协同：本模块定级裁决，PRECHECK 定位具体项。
> 完整性门控静默执行；无未解决 CRITICAL 才允许「可送审」。

## 核心流程

### Step 0 · 场景适配
学位层次（博士/硕士，工作量与创新门槛不同）+ 载体（Markdown + Pandoc，非 LaTeX）。

### 五维审查
| 维度 | 要点 |
|---|---|
| 1 宏观逻辑 | 绪论漏斗完整；贡献↔方法↔章节一一对应；实验验主论断；running example 一致；头条结果有消融隔离；论断匹配证据（CRITICAL 断裂） |
| 2 写作细节 | 每段主题句（AXES）；无孤儿段；段不过 10 行；摘要三要素 |
| 3 中文语法与表达 | 引用 `ACADEMIC_STYLE_ZH.md` 具体规则；术语一致；`本文/我们` 统一 |
| 4 Markdown/Pandoc 格式 | 标题层级连续；`$...$`/`$$...$$`；题注自明；`[@key]` 保留；GB/T 7714 |
| 5 图表质量 | 矢量、字号、色盲友好、题注含发现、无 chartjunk |

**检索接地**（有检索能力时）：新颖性核验（列 3–5 篇最接近工作，按差异轴比）+ 引用完整性（缺关键基线/经典/近期综述 = MAJOR）。

### 严重度
CRITICAL/P0 阻断送审 · MAJOR/P1 首轮必被指出 · MINOR/P2 润色级。
禁词与破折号全文扫描：出现 3+ 次 = MAJOR；破折号作连接词默认 MAJOR。

### 输出
摘要（CRITICAL/MAJOR/MINOR 计数 + 最优先三项）→ 五维表（发现引用原文 / 严重度 / 建议修复）→ 禁词扫描 → 评分（1–10）→ 送审建议（可送审 / 再打磨 / 需重大修改）。
评分一致：9/10 要求 0 CRITICAL 且 ≤2 MAJOR。

> Full details: see [`../REVIEW_GUIDE.md`](../REVIEW_GUIDE.md), [`../CITATION_VERIFICATION.md`](../CITATION_VERIFICATION.md), [`PRECHECK.md`](PRECHECK.md)

> 内容层规则（五维表第 1/2/5 维的证据映射与图表承载）：见 [`../CONTENT_RULES.md`](../CONTENT_RULES.md)。
