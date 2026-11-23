# 与 Best-Paper-Writing-Skill 的内容规则对照（2026-11-23）

## 触发与来源

- niky 指令：抓取推文 <https://x.com/fngly343149/status/2124679935302480122> 全部内容存到 `D:\WritingSkills`，参考其中的内容规则修改本 SKILL。
- 推文：福叔 @fngly343149，2026-11-23 09:42（北京时间），点赞 758 / 收藏 1024 / 浏览 3.6 万；配图为仓库卡片截图（424★）。归档：`D:\WritingSkills\_tweet_2124679935302480122\`（`tweet.md`、`tweet_fxtwitter.json`、`tweet_photo_1.jpg`、`author_avatar.jpg`）。
- 仓库：`gulucaptain/Best-Paper-Writing-Skill` @ main `b9eff99a`，git clone 到 `D:\WritingSkills\Best-Paper-Writing-Skill\`（1.2 MB，含 SKILL.md、references/、scripts/、assets/、evals/、data/、template/CVPR2027/）。
- 语料口径：60 篇 2021–2025 CVPR/ICCV/NeurIPS 获奖论文（CVPR 22 / ICCV 12 / NeurIPS 26）逐句标注统计；55 篇拟合规则、5 篇（2024）留出测试；配图排版规则来自 44 篇配图统计。

## 规则提取与可迁移性判定

| 来源规则 | 判定 | 落点 |
|---|---|---|
| 主张-证据映射（claim map：主张/证据/最强许可措辞/头条数字分级；同一主张只出现一次、各处强度一致） | ✅ 迁移 | `CONTENT_RULES.md` §1；SKILL.md Content Rules 节 |
| 绪论漏斗：具体肯定前人 → 缺口含失效条件+原因 → 对问题的观察（洞察）→ 方法 → 结果；最相近工作给可核查差异 | ✅ 迁移（强化 `logic` A3） | §2 |
| 方法章组件按「需要 → 机制 → 性质」展开、写前后件关系不并列、机制缺失留白不编抽象名词 | ✅ 迁移 | §3 |
| 消融与主张一一对应（evidence map：主张→方法小节→实验→消融） | ✅ 迁移（补 `experiment` 缺口） | §4 |
| 配图规划表（每图承载哪个主张/位置/素材/状态/题注首句；一图一主张；结果图留白不编造） | ✅ 迁移（判断驱动，无脚本） | §5 |
| 统计口径只作线索、有上下限、不向均值磨平；保留有记忆点的枢轴句 | ✅ 迁移（与「命中 ≠ 改写判据」衔接） | §6 |
| 无证据主张软化或占位（不编造数字/基线/引用） | ✅ 迁移（占位符统一为 `【待补证】`） | §1/§4 |
| CVPR author kit / LaTeX / TikZ 资产、`main.tex` 口径脚本 | ❌ 不迁移（Markdown + Pandoc 载体） | §7 |
| 英文「no dashes」「20–24 words」「no trailing participial clause」原样阈值、we/our voice | ❌ 不迁移（中文语域不同） | §7 |
| 「局限/失败案例不进摘要与绪论」 | ❌ 不迁移（禁改清单保护绪论研究意义句） | §7 |
| Figure 1 八类路由、第 1 页通栏、L1–L8 论文路由、venue fit、rebuttal、投稿门控 | ❌ 不迁移（英文会议专属） | §7 |
| `intake_form.html`、`report.md`、留出盲评集、exemplars 英文范例句 | ❌ 不迁移（不新增脚本/表单/资产；范例句有版权且会污染中文语域） | §7 |
| 推文自身的营销文案模板（`·机制/·结果`、`谁该用：`、`判断：`、星数社会证明） | ❌ 禁止写入论文正文 | §6 |

## 与 thesis-zh 现有能力的缺口判定

- 已有（不动）：AXES 段落模型、五维审查第 1 维「贡献↔方法↔章节一一对应；头条结果有消融隔离」、B3 归因分析、B4 结果-文献回溯、CW Boundaries 证据纪律与禁编造、CAPTION_GUIDE 题注。
- 本次补齐：跨章节统一的主张-证据映射表；缺口「条件+原因」与洞察的具体化标准；组件按关系展开；图表规划表（先规划后画）；统计口径只作线索的明示；英文顶会专属规则与营销模板的显式黑名单。

## 改动落点

| 文件 | 改动 |
|---|---|
| `SKILL.md` | description 追加触发短语；Module Router `logic`/`experiment`/`review`/`polish` 的 Read next 加 `+ CONTENT_RULES`；Workflow 新增 2b；新增「Content Rules（内容层规则）」节（4 条 + 边界）；Reference Map +2 行；Examples +1 条 |
| `references/CONTENT_RULES.md` | 新增：内容层规则全量细则（§0 接口、§1–6 规则、§7 不可迁移清单、§8 交付前检查清单） |
| `references/modules/{LOGIC,EXPERIMENT,REVIEW}.md` | 末尾各 +1 行指针；EXPERIMENT 附 LaTeX 示例仅限 `.tex` 的注记 |
| `agents/openai.yaml` | short_description 加 claim-evidence & figure planning |
| `test-prompts.json` | +2 例（id7 内容层问题、id8 消融对齐与图表规划） |
| `evals/evals.json` | +2 例（id17、id18，含正则断言） |

## 验证

- `test-prompts.json` 8 例 / `evals.json` 18 例 `json.loads` 通过（evals.json 曾被 json.dumps 重排，已 `git checkout` 恢复后按原格式精确追加）。
- frontmatter：`name: thesis-zh` 存在；description 830 字符 < 1024；SKILL.md 163 行 < 500；磁盘 17838 B ≈ 1.491× 基线（基线 ≈ 11966 B，1.5× 门禁 = 17949 B），未破达尔文体积门禁。
- `git diff --check` 无空白错误；`.workbuddy/` 按惯例不提交。
- 未提交、未推送（等 niky 指令）；未改 `deai_check.py` 等脚本（延续 11-15「不改核心功能」约束）。

## 下一步（可选）

- 若要本 skill 具备英文会议论文能力，建议另建独立 skill 而非扩本 skill（Do Not Use 已划界）。
- `references/CAPTION_GUIDE.md`、`modules/EXPERIMENT.md` 的 LaTeX 示例为历史遗留，已加注记，如需彻底清理另行确认。
