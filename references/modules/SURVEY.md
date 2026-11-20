# Survey Module Reference — 文献调研与综述综合

Purpose: 为选题/综述章做综述级深度调研：冻结研究问题 → 多视角对抗检索 → 逐条引用核验 → MECE 综合 → 自对抗审查。

> 🔴 **能力前提**：必须有检索能力（学术工具 > 学术索引网页检索 > 公开 API）。**完全无检索则不运行**，如实说明，不靠记忆写综述。
> 引用核验按 [`../CITATION_VERIFICATION.md`](../CITATION_VERIFICATION.md)；核验不通过的文献不进综合。

## 核心流程

| 阶段 | 动作 | 关键约束 |
|---|---|---|
| Step 0 冻结 Brief | 课题 → 2–3 个可回答的 RQ + 角度 + 读者 | 之后每步对齐 Brief，不漂移 |
| Phase 1 侦察 | 3–5 个检索视角（主流/批评/邻近/方法/应用），先宽后窄；可并行子代理 | 合并后查盲区：无返回视角、未覆盖子方向、被高频引用却未入池的工作 |
| 引用核验 | 每条候选按 `CITATION_VERIFICATION.md` 五级状态核验 | 每个子方向覆盖 ≥3 篇；不设总量配额；不通过不进语料 |
| Phase 2 综合 | 抽发现 → MECE 聚类 → 分配文献 → 逐分支串行写 | 句内交叉比较强制；矛盾用条件分析，不取平均 |
| 自对抗 | 回问 3 问 + 视角遗漏检查 + 让步规则 | 反证确凿须显式让步，不以「待研究」模糊带过 |
| 六门迭代 | Angle / Coverage / Citation / Taxonomy / Calibration / Weaving | Coverage/Citation 失败 → 定向补检 + 增量更新，非推倒重来 |

**hedge 阶梯**：强（多项一致）/ 中（两三项，有边界）/ 弱（一两项或仅机制）/ 无证据（检索无果）——论断强度永不超出证据。

**输出**：写入工作区 Markdown 的调研报告（摘要 / RQ 绪论 / 方法论 / MECE 分类 / 各分支比较表 / 跨分支讨论 / 开放问题 / 逐条答 RQ / 参考文献）。
报告允许统一「未确认标记」；论文正文禁止——不可混用。

## Quick Start

```
输入：课题 or RQ + （可选）目标学位层次/读者
输出：工作区 .md 调研报告 + 检索能力降级说明
```

> Full details: see [`../SURVEY_GUIDE.md`](../SURVEY_GUIDE.md), [`../CITATION_VERIFICATION.md`](../CITATION_VERIFICATION.md)
