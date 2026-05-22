# Pandoc 导出指南

## 概述

使用 Pandoc 将 Markdown 格式的中文学位论文导出为 PDF 或 DOCX。

## 工具链

### PDF 输出（推荐）

需要：Pandoc + XeLaTeX（TeX Live / MiKTeX）

```bash
pandoc thesis.md -o thesis.pdf \
  --pdf-engine=xelatex \
  -V CJKmainfont=SimSun \
  -V mainfont="Times New Roman" \
  -V geometry:margin=2.5cm \
  --bibliography=refs.bib \
  --citeproc \
  --number-sections \
  --toc
```

### DOCX 输出

仅需 Pandoc，无需 LaTeX 环境。

```bash
pandoc thesis.md -o thesis.docx \
  --bibliography=refs.bib \
  --citeproc \
  --number-sections \
  --toc
```

## 多文件项目

对于多文件论文目录，按文件名排序拼接：

```bash
pandoc chapters/*.md -o thesis.pdf --pdf-engine=xelatex ...
```

建议文件命名：
- `00-abstract.md`
- `01-introduction.md`
- `02-related-work.md`
- `03-method.md`
- `04-experiments.md`
- `05-conclusion.md`
- `06-acknowledgment.md`

## 参考文献

使用 Pandoc 风格的引用：

```markdown
根据近年研究 [@smith2020; @jones2021]，该方法已被证明有效。
```

配合 `.bib` 文件和 `--citeproc` 选项自动生成参考文献列表。

## 常见问题

| 问题 | 解决方案 |
|------|---------|
| 中文字体缺失 | 指定 `-V CJKmainfont=SimSun` 或系统中可用的中文字体 |
| 公式渲染异常 | 确保使用 `--pdf-engine=xelatex` 而非默认引擎 |
| 参考文献未渲染 | 添加 `--citeproc --bibliography=refs.bib` |
| 文件顺序错误 | 用数字前缀命名文件（01-, 02-, ...）|
