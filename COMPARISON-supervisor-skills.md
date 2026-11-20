# 写作能力对比：Supervisor-Skills vs 本项目（thesis-zh）

> 对比对象：[HKUSTDial/Supervisor-Skills](https://github.com/HKUSTDial/Supervisor-Skills)（v2.1，CC BY-NC-SA 4.0）写作相关技能 × 本项目 `thesis-zh`（Markdown 中文学位论文助手）。
> 本文只做「能力对照 + 缺口判定 + 补充落点」记录；具体方法已提炼、适配学位论文语境后写入 `references/` 与 `references/modules/`。

## 一、定位差异（决定哪些能直接搬、哪些要改写）

| 维度 | Supervisor-Skills | 本项目 thesis-zh |
| --- | --- | --- |
| 产物 | 英文会议/期刊论文（SIGMOD/VLDB/ICML/NeurIPS） | 中文学位论文（Markdown + Pandoc，GB/T 7714） |
| 阶段 | Idea → 调研 → 写作 → 润色 → 投稿 → Rebuttal 全周期 | **已有论文**的定向问题检查与改写 |
| 机制 | 纯 Prompt/Skill（LLM 判断为主） | 脚本驱动（`scripts/*.py`）+ 审阅友好标注 + 唯一真源边界 |
| 强项 | 五维评估、对抗式调研、证据门控、严重度门控 | Chinese Writing Boundaries（禁改清单/证据纪律/Quick Checks/CHECKPOINT）、盲审自查 |

结论：Supervisor-Skills 的**方法论骨架**可迁移，但**英文会议论文的具体规则**（LaTeX 规则、英文语法、venue fit、rebuttal、投稿门控）不可直接套用，必须改写为学位论文语境。

## 二、逐项对照

| 写作能力 | Supervisor-Skills 对应技能 | 本项目现状 | 判定 |
| --- | --- | --- | --- |
| 选题评估 | `idea-evaluator`：五维（更高/更快/更强/更省/更广）、致命缺陷 10 条、生命周期与能力匹配、范式转换 4 问、可行性、三档裁决、integrity gate | 无；Do Not Use 仅排除「从零写」，无选题论证能力 | 🔴 缺 → 补 `topic` |
| 文献调研与综述综合 | `deep-research`：冻结 RQ、多视角对抗检索、引用核验协议、MECE 综合、自对抗审查、六道门、hedge 校准 | 仅 `bibliography`（格式校验）+ `logic` A1–A4（综述质量**检查**）；无「调研→核验→综合」生产流程 | 🔴 缺 → 补 `survey` |
| 引用真实性核验 | `paper-writer` verification ladder：三级能力阶梯、VERIFIED/MISMATCH/NOT_FOUND/OVERCLAIM/INCONCLUSIVE 五状态、收敛规则 | `verify_bib.py`/`online_bib_verify.py` 查格式与在线条目，但无「独立核验 + 状态分级 + 收敛」方法论 | 🔴 缺 → 补 `references/CITATION_VERIFICATION.md` |
| 忠于原意的润色 | `paper-polish`：忠于原意、禁编造、轻触默认、语气校准（hedging 阶梯）、分节惯例、phrasebank、中译英、交付格式 | `deai` 模块 + Chinese Writing Boundaries 已覆盖「去 AI 腔/证据纪律/禁改」，但**无** hedging 阶梯词表、分节写作惯例、按证据强度的动词库 | 🟠 部分缺 → 补 `polish` |
| 送审前总核查 | `pre-submission-reviewer`：五维审查、CRITICAL/MAJOR/MINOR、完整性门控 [inspection]/[attestation]、禁词+破折号、评分裁决 | 9 个分散检查模块 + 孤儿模块 `PRECHECK.md`（盲审自查，已是 P0/P1/P2 严重度，但未注册路由）；无统一总审稿与裁决 | 🟠 部分缺 → 补 `review`（不重复 `paper-audit` 的投稿门控） |
| 绪论/正文从零起草 | `intro-drafter`、`paper-writer`、`tech/benchmark-paper-template` | Do Not Use 明确排除「从零写一篇学位论文」 | ⚪ 定位差异，不补（保持边界） |
| 图表设计 / Draw.io 重建 | `figure-designer`、`drawio-reconstruction` | 有 `CAPTION_GUIDE.md`，无图表生成/重建 | ⚪ 非本次「写作」范围，不补 |
| Rebuttal | `rebuttal-guidance` | 无；学位论文对应「答辩」，机制不同 | ⚪ 不补 |

## 三、补充落点（本次实际改动）

| 新增模块 | 触发 | 深度参考 | 来源方法 |
| --- | --- | --- | --- |
| `topic` | 选题/开题可行性论证、评选题方向 | `references/TOPIC_EVALUATION.md` | idea-evaluator（五维、致命缺陷、能力匹配、范式探测、裁决） |
| `survey` | 文献调研、写/改综述章节的调研综合 | `references/SURVEY_GUIDE.md` + `references/CITATION_VERIFICATION.md` | deep-research（冻结 RQ、多视角、MECE、六门、自对抗） |
| `polish` | 忠于原意的语言润色、语气校准、中译英 | `references/POLISH_GUIDE.md` | paper-polish（轻触默认、hedging 阶梯、分节惯例、phrasebank） |
| `review` | 送审/答辩前统一核查与裁决 | `references/REVIEW_GUIDE.md` + `references/CITATION_VERIFICATION.md` | pre-submission-reviewer（严重度、完整性门控、禁词、评分裁决） |

**边界纪律**：`polish`/`review` 的改写动作一律服从 `SKILL.md §Chinese Writing Boundaries`（唯一真源）；与 `deai`（去 AI 痕迹）分工——`deai` 负责诊断+削减 AI 痕迹，`polish` 负责通用语言润色，二者共用同一套禁改清单与证据纪律。`review` 只做学位论文送审/答辩前核查，英文期刊投稿门控仍走 `paper-audit`。

## 四、未补项及理由

- 从零起草正文：与项目「处理已有论文」定位冲突，保持 Do Not Use 排除。
- Rebuttal / 图表重建：非用户点名的「写作（选题·润色·核查）」范围，且机制与学位论文不对口。
- 英文语法规则：学位论文主体为中文，英文仅摘要；相关对照表已收进 `POLISH_GUIDE.md` 附录，不单列模块。
