#!/usr/bin/env python3
"""
Pandoc Export Script - 中文学位论文 Markdown 导出

将 Markdown 格式的论文导出为 PDF 或 DOCX。
支持 Pandoc + XeLaTeX（PDF）或 Pandoc + DOCX 引擎。

Usage:
    uv run python export.py thesis_dir/ --format pdf
    uv run python export.py thesis.md --format docx
    uv run python export.py thesis_dir/ --format pdf --bib references.bib
    uv run python export.py thesis_dir/ --check     # 仅检查工具链
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional


class PandocExporter:
    """Export Markdown thesis to PDF/DOCX via Pandoc."""

    def __init__(
        self,
        source: str,
        output_format: str = "pdf",
        bib_file: Optional[str] = None,
        csl_file: Optional[str] = None,
        template: Optional[str] = None,
        output_file: Optional[str] = None,
    ):
        self.source_path = Path(source).resolve()
        self.output_format = output_format
        self.bib_file = bib_file
        self.csl_file = csl_file
        self.template = template
        self.output_file = output_file

        if self.source_path.is_dir():
            self.work_dir = self.source_path
            self.md_files = self._collect_md_files()
        else:
            self.work_dir = self.source_path.parent
            self.md_files = [self.source_path]

    def _collect_md_files(self) -> list[Path]:
        """Collect and sort .md files from a directory."""
        md_files = sorted(self.source_path.rglob("*.md"))
        # Filter out non-thesis files
        filtered = []
        for f in md_files:
            name_lower = f.stem.lower()
            if name_lower in ("readme", "changelog", "license", "contributing"):
                continue
            filtered.append(f)
        return filtered

    def check_tools(self) -> tuple[bool, list[str]]:
        """Check if required tools are available."""
        issues = []

        if not shutil.which("pandoc"):
            issues.append("pandoc not found. Install from https://pandoc.org/installing.html")

        if self.output_format == "pdf":
            if not shutil.which("xelatex"):
                issues.append(
                    "xelatex not found. Install TeX Live or MiKTeX for PDF output. "
                    "Or use --format docx as alternative."
                )

        return len(issues) == 0, issues

    def _build_pandoc_cmd(self) -> list[str]:
        """Build the Pandoc command line."""
        output = self.output_file
        if not output:
            stem = self.source_path.stem if self.source_path.is_file() else "thesis"
            output = str(self.work_dir / f"{stem}.{self.output_format}")

        cmd = ["pandoc"]

        # Input files
        cmd.extend(str(f) for f in self.md_files)

        # Output
        cmd.extend(["-o", output])

        # PDF engine for Chinese support
        if self.output_format == "pdf":
            cmd.extend(["--pdf-engine=xelatex"])
            # CJK font settings
            cmd.extend([
                "-V", "CJKmainfont=SimSun",
                "-V", "mainfont=Times New Roman",
                "-V", "geometry:margin=2.5cm",
                "-V", "fontsize=12pt",
                "-V", "documentclass=ctexart",
            ])

        # Bibliography
        if self.bib_file:
            cmd.extend(["--bibliography", self.bib_file])
            cmd.append("--citeproc")
            if self.csl_file:
                cmd.extend(["--csl", self.csl_file])

        # Template
        if self.template:
            cmd.extend(["--template", self.template])

        # Common options
        cmd.extend([
            "--standalone",
            "--number-sections",
            "--toc",
        ])

        return cmd

    def export(self) -> int:
        """Run the export."""
        # Check tools
        ok, issues = self.check_tools()
        if not ok:
            for issue in issues:
                print(f"[ERROR] {issue}")
            return 1

        if not self.md_files:
            print("[ERROR] No .md files found to export")
            return 1

        print(f"[INFO] Exporting {len(self.md_files)} file(s) to {self.output_format.upper()}")
        print(f"[INFO] Working directory: {self.work_dir}")

        # Auto-detect .bib file if not specified
        if not self.bib_file:
            for bib_name in ["references.bib", "refs.bib", "bibliography.bib", "ref.bib"]:
                bib_path = self.work_dir / bib_name
                if bib_path.exists():
                    self.bib_file = str(bib_path)
                    print(f"[INFO] Auto-detected bibliography: {bib_name}")
                    break

        cmd = self._build_pandoc_cmd()
        print(f"[INFO] Command: {' '.join(cmd)}")

        try:
            result = subprocess.run(
                cmd,
                cwd=self.work_dir,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )

            if result.returncode == 0:
                output_file = self.output_file or f"thesis.{self.output_format}"
                print(f"\n[SUCCESS] Output: {output_file}")
                if result.stderr:
                    # Pandoc warnings
                    warnings = [l for l in result.stderr.split("\n") if l.strip()]
                    if warnings:
                        print(f"[WARNING] Pandoc warnings ({len(warnings)}):")
                        for w in warnings[:5]:
                            print(f"  {w}")
            else:
                print(f"\n[ERROR] Export failed with exit code {result.returncode}")
                if result.stderr:
                    print("[STDERR]:")
                    for line in result.stderr.split("\n")[:20]:
                        if line.strip():
                            print(f"  {line}")

            return result.returncode

        except FileNotFoundError:
            print("[ERROR] pandoc not found. Please install Pandoc.")
            return 1
        except Exception as e:
            print(f"[ERROR] {e}")
            return 1


def main():
    parser = argparse.ArgumentParser(
        description="Markdown 中文学位论文导出（Pandoc）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  uv run python export.py thesis_dir/ --format pdf
  uv run python export.py thesis.md --format docx
  uv run python export.py thesis_dir/ --format pdf --bib refs.bib
  uv run python export.py thesis_dir/ --check
        """,
    )
    parser.add_argument("source", help="Markdown 文件或论文目录")
    parser.add_argument(
        "--format", "-f",
        choices=["pdf", "docx"],
        default="pdf",
        help="输出格式 (default: pdf)",
    )
    parser.add_argument("--bib", "-b", help="参考文献 .bib 文件路径")
    parser.add_argument("--csl", help="CSL 引用样式文件路径")
    parser.add_argument("--template", "-t", help="Pandoc 模板文件")
    parser.add_argument("--output", "-o", help="输出文件路径")
    parser.add_argument(
        "--check", action="store_true", help="仅检查工具链是否可用"
    )

    args = parser.parse_args()

    source_path = Path(args.source)
    if not source_path.exists():
        print(f"[ERROR] 路径不存在: {args.source}")
        sys.exit(1)

    exporter = PandocExporter(
        args.source,
        output_format=args.format,
        bib_file=args.bib,
        csl_file=args.csl,
        template=args.template,
        output_file=args.output,
    )

    if args.check:
        ok, issues = exporter.check_tools()
        if ok:
            print("[SUCCESS] All required tools are available")
            print(f"  pandoc: {shutil.which('pandoc')}")
            if args.format == "pdf":
                print(f"  xelatex: {shutil.which('xelatex')}")
        else:
            for issue in issues:
                print(f"[ERROR] {issue}")
        sys.exit(0 if ok else 1)

    sys.exit(exporter.export())


if __name__ == "__main__":
    import io, os
    if os.name == "nt":
        for stream in (sys.stdout, sys.stderr):
            if hasattr(stream, "reconfigure"):
                stream.reconfigure(encoding="utf-8")
    main()
