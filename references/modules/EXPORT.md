# Export Module Reference

Purpose: Export Markdown thesis to PDF or DOCX via Pandoc.

## Tool Requirements

| Tool | Required For | Install |
|------|-------------|---------|
| Pandoc | All exports | https://pandoc.org/installing.html |
| XeLaTeX | PDF output (CJK support) | TeX Live or MiKTeX |

## Quick Start

```bash
# Check tools
uv run python export.py thesis_dir/ --check

# Export to PDF
uv run python export.py thesis_dir/ --format pdf

# Export to DOCX
uv run python export.py thesis_dir/ --format docx

# With bibliography
uv run python export.py thesis_dir/ --format pdf --bib refs.bib
```

## Common Issues

| Problem | Solution |
|---------|----------|
| Chinese font not found | Install SimSun or specify CJK font via -V CJKmainfont=xxx |
| Bibliography not rendered | Ensure --citeproc flag and valid .bib file |
| Missing pandoc | Install from https://pandoc.org/installing.html |

## Multi-file Projects

When pointing to a directory, the export script will:
1. Collect all `.md` files recursively
2. Sort them alphabetically
3. Auto-detect `.bib` files (references.bib, refs.bib)
4. Concatenate and export as single document

> Tip: Prefix filenames with numbers (01-introduction.md, 02-related.md) for correct ordering.
