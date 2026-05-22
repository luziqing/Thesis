# Format Module Reference

Purpose: Check surface-level errors in Chinese thesis files: typos, punctuation, formatting.

## Check Priority

| Priority | Category | Severity | Description |
|----------|----------|----------|-------------|
| **P0** | 错别字 | error | 形近字/音近字混淆、成语误用、的地得误用、赘余表达 |
| **P1** | 标点错误 | error/warning | 中英标点混用、连续标点、括号引号不配对、段末缺标点、全角字母 |
| **P2** | 格式问题 | warning/info | 标题层级跳跃、标题前缺空行、引用格式（仅 Markdown） |
| **P3** | 风格建议 | info | 口语化表达、主观代词、夸张表述、中英文间空格（需 --strict） |

## Usage

```bash
# 默认检查（P0 + P1 + P2）
uv run python check_format.py thesis.md

# 严格模式（含 P3 风格建议）
uv run python check_format.py thesis.md --strict

# 扫描整个目录
uv run python check_format.py thesis_dir/ --strict

# JSON 输出
uv run python check_format.py thesis_dir/ --json
```

## P0 错别字规则 (30+)

- 形近字：己→已、侯→候、帐→账、精→经、座→坐
- 音近字：以→已、做→作、专→钻、题→提
- 成语：长期以往→长此以往、迫不急待→迫不及待 等 8 条
- 的地得：修饰动词用"地"（认真的分析→认真地分析）10 条
- 赘余：擅长于、大约…左右、可以能够
- 学术规范：其它→其他

## P1 标点规则

- 中英标点混用（中文后英文逗号/句号、英文标点后跟中文）
- 连续标点（，，、。。）
- 括号/引号配对检查 5 种：（）【】《》""''
- 段落末尾缺标点
- 全角英文字母/数字

> Full details: see [`../GB_STANDARD.md`](../GB_STANDARD.md)
