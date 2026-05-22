# 示例：导出与结构检查

用户请求：
帮我把这个 Markdown 论文目录导出为 PDF，顺便梳理一下结构是否完整。

推荐模块顺序：
1. `structure`
2. `export`

命令：
```bash
uv run python $SKILL_DIR/scripts/map_structure.py thesis_dir/
uv run python $SKILL_DIR/scripts/export.py thesis_dir/ --format pdf
```

预期输出：
- 论文结构树和完整性检查结果。
- PDF 导出结果或失败时的排查建议。
