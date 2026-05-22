#!/usr/bin/env python3
"""
Thesis Structure Mapper - Map multi-file thesis structure

Supports both LaTeX multi-file projects (\\input/\\include) and
Markdown multi-file projects (directory scanning).

Usage:
    uv run python map_structure.py thesis_dir/
    uv run python map_structure.py thesis.md
    uv run python map_structure.py main.tex --json
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Optional


class ThesisStructureMapper:
    """Map thesis file structure for LaTeX or Markdown projects."""

    # File type detection patterns (universal)
    FILE_TYPES = {
        "cover": ["cover", "titlepage", "frontpage", "封面"],
        "abstract": ["abstract", "abs", "摘要"],
        "declaration": ["declaration", "authorization", "声明", "原创性"],
        "toc": ["toc", "contents", "目录"],
        "symbol": ["symbol", "notation", "nomenclature", "符号", "术语"],
        "chapter": ["chap", "chapter", "章", "ch"],
        "appendix": ["appendix", "app", "附录"],
        "bibliography": ["bib", "ref", "reference", "参考文献"],
        "acknowledgment": ["ack", "thanks", "致谢", "后记"],
        "resume": ["resume", "publication", "简历", "论文目录", "发表"],
        "introduction": ["intro", "绪论", "引言"],
        "conclusion": ["conclusion", "总结", "结论"],
    }

    # Known LaTeX university templates
    TEMPLATES = {
        "thuthesis": {
            "pattern": r"\\documentclass.*\{thuthesis\}",
            "name": "Tsinghua University (thuthesis)",
            "figure_format": "图 3-1",
        },
        "pkuthss": {
            "pattern": r"\\documentclass.*\{pkuthss\}",
            "name": "Peking University (pkuthss)",
            "figure_format": "图3.1",
        },
        "ustcthesis": {
            "pattern": r"\\documentclass.*\{ustcthesis\}",
            "name": "USTC (ustcthesis)",
            "figure_format": "图 3.1",
        },
        "fduthesis": {
            "pattern": r"\\documentclass.*\{fduthesis\}",
            "name": "Fudan University (fduthesis)",
            "figure_format": "图 3.1",
        },
        "ctexbook": {
            "pattern": r"\\documentclass.*\{ctexbook\}",
            "name": "Generic Chinese Book (ctexbook)",
            "figure_format": "图 3.1",
        },
    }

    def __init__(self, main_file: str):
        self.main_path = Path(main_file).resolve()
        if self.main_path.is_dir():
            self.root_dir = self.main_path
            self.is_directory_mode = True
        else:
            self.root_dir = self.main_path.parent
            self.is_directory_mode = False
        self.visited: set[Path] = set()
        self.structure: list[dict] = []
        self.template: Optional[str] = None

    def map(self) -> list[dict]:
        """Map the thesis structure."""
        self.structure = []
        self.visited = set()

        if self.is_directory_mode:
            self._scan_directory()
        elif self.main_path.suffix.lower() in (".md",):
            self._scan_directory()  # For .md files, scan the directory
        else:
            self._parse_latex_file(self.main_path, level=0)

        return self.structure

    def _scan_directory(self):
        """Scan directory for .md files and build structure."""
        md_files = sorted(self.root_dir.rglob("*.md"))

        for md_file in md_files:
            # Skip common non-thesis files
            name_lower = md_file.stem.lower()
            if name_lower in ("readme", "changelog", "license", "contributing"):
                continue

            file_type = self._detect_file_type(md_file)

            # Try to extract the top-level heading for better labeling
            heading = self._extract_first_heading(md_file)

            self.structure.append({
                "file": str(md_file.relative_to(self.root_dir)),
                "level": 0,
                "type": file_type,
                "exists": True,
                "heading": heading,
            })

    def _extract_first_heading(self, md_file: Path) -> Optional[str]:
        """Extract the first # heading from a Markdown file."""
        try:
            content = md_file.read_text(encoding="utf-8", errors="ignore")
            match = re.search(r"^#\s+(.+?)\s*$", content, re.MULTILINE)
            if match:
                return match.group(1).strip()
        except Exception:
            pass
        return None

    def _parse_latex_file(self, tex_file: Path, level: int):
        """Recursively parse a LaTeX file for includes."""
        if tex_file in self.visited:
            return
        self.visited.add(tex_file)

        if not tex_file.exists():
            self.structure.append({
                "file": str(tex_file.relative_to(self.root_dir))
                if tex_file.is_relative_to(self.root_dir)
                else str(tex_file),
                "level": level,
                "type": "missing",
                "exists": False,
            })
            return

        file_type = self._detect_file_type(tex_file)
        self.structure.append({
            "file": str(tex_file.relative_to(self.root_dir)),
            "level": level,
            "type": file_type,
            "exists": True,
        })

        try:
            content = tex_file.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return

        if level == 0:
            self.template = self._detect_template(content)

        patterns = [
            (r"\\input\{([^}]+)\}", "input"),
            (r"\\include\{([^}]+)\}", "include"),
            (r"\\subfile\{([^}]+)\}", "subfile"),
        ]

        for pattern, _include_type in patterns:
            for match in re.finditer(pattern, content):
                included = match.group(1)
                if not included.endswith(".tex"):
                    included += ".tex"
                included_path = (tex_file.parent / included).resolve()
                if not included_path.exists():
                    included_path = (self.root_dir / included).resolve()
                self._parse_latex_file(included_path, level + 1)

    def _detect_file_type(self, file_path: Path) -> str:
        """Detect the type of a thesis file based on name and content."""
        name = file_path.stem.lower()

        for file_type, patterns in self.FILE_TYPES.items():
            for pattern in patterns:
                if pattern in name:
                    if file_type == "chapter":
                        match = re.search(r"(\d+)", name)
                        if match:
                            return f"第{match.group(1)}章"
                    return file_type

        # For Markdown files, try reading first heading
        if file_path.suffix.lower() == ".md":
            heading = self._extract_first_heading(file_path)
            if heading:
                heading_lower = heading.lower()
                for section_name, keywords in {
                    "introduction": ["绪论", "引言"],
                    "abstract": ["摘要"],
                    "conclusion": ["结论", "总结"],
                    "acknowledgment": ["致谢"],
                    "bibliography": ["参考文献"],
                }.items():
                    if any(kw in heading_lower for kw in keywords):
                        return section_name

        return "other"

    def _detect_template(self, content: str) -> Optional[str]:
        """Detect university template from document class."""
        for template_id, info in self.TEMPLATES.items():
            if re.search(info["pattern"], content):
                return template_id
        return None

    def get_template_info(self) -> Optional[dict]:
        """Get information about detected template."""
        if self.template and self.template in self.TEMPLATES:
            return self.TEMPLATES[self.template]
        return None

    def get_processing_order(self) -> list[str]:
        """Get recommended processing order."""
        if not self.structure:
            self.map()

        priority = {
            "cover": 0,
            "declaration": 1,
            "abstract": 2,
            "toc": 3,
            "symbol": 4,
            "introduction": 5,
            "第1章": 5,
            "第2章": 6,
            "第3章": 7,
            "第4章": 8,
            "第5章": 9,
            "chapter": 10,
            "appendix": 11,
            "bibliography": 12,
            "acknowledgment": 13,
            "conclusion": 14,
            "resume": 15,
            "other": 16,
            "missing": 99,
        }

        def get_priority(item):
            t = item["type"]
            for key in priority:
                if t.startswith(key) or t == key:
                    return priority[key]
            return priority["other"]

        sorted_structure = sorted(self.structure, key=get_priority)
        return [item["file"] for item in sorted_structure if item["exists"]]

    def check_completeness(self) -> dict:
        """Check thesis structure completeness."""
        if not self.structure:
            self.map()

        found_types = {item["type"] for item in self.structure if item["exists"]}

        required = ["abstract", "bibliography", "acknowledgment"]
        recommended = ["declaration", "symbol", "resume"]

        # Check for introduction
        has_intro = any(
            ft in found_types
            for ft in ["introduction", "第1章"]
        ) or any(
            ft.startswith("第") and "1" in ft
            for ft in found_types
        )

        if not has_intro:
            # Also check headings in the files
            for item in self.structure:
                if item.get("heading") and any(
                    kw in item["heading"] for kw in ["绪论", "引言"]
                ):
                    has_intro = True
                    break

        missing_required = [
            t for t in required if not any(ft.startswith(t) or ft == t for ft in found_types)
        ]
        missing_recommended = [
            t for t in recommended if not any(ft.startswith(t) or ft == t for ft in found_types)
        ]

        chapters = [
            item for item in self.structure
            if item["type"].startswith("第") or item["type"] == "chapter"
        ]

        return {
            "complete": len(missing_required) == 0 and has_intro,
            "missing_required": missing_required,
            "missing_recommended": missing_recommended,
            "chapter_count": len(chapters),
            "has_introduction": has_intro,
        }

    def generate_tree(self) -> str:
        """Generate a tree-style visualization."""
        if not self.structure:
            self.map()

        lines = []
        lines.append("=" * 60)
        lines.append("Thesis Structure / 论文结构树")
        lines.append("=" * 60)

        if self.template:
            template_info = self.get_template_info()
            lines.append(f"Template: {template_info['name'] if template_info else self.template}")
            lines.append("")

        mode = "Markdown (directory scan)" if self.is_directory_mode else "LaTeX (file includes)"
        lines.append(f"Mode: {mode}")
        lines.append(f"Root: {self.root_dir}")
        lines.append("")

        for i, item in enumerate(self.structure):
            indent = "  " * item["level"]
            prefix = "├── " if i < len(self.structure) - 1 else "└── "
            prefix = indent + prefix if item["level"] > 0 else ""

            status = "" if item["exists"] else " [MISSING]"
            type_label = f"({item['type']})"
            heading = f" → {item['heading']}" if item.get("heading") else ""

            lines.append(f"{prefix}{item['file']} {type_label}{heading}{status}")

        # Completeness check
        completeness = self.check_completeness()
        lines.append("")
        lines.append("-" * 60)
        lines.append("Completeness Check / 完整性检查")
        lines.append("-" * 60)
        lines.append(f"Status: {'✅ Complete' if completeness['complete'] else '⚠️ Incomplete'}")
        lines.append(f"Chapters: {completeness['chapter_count']}")
        lines.append(f"Introduction: {'✅' if completeness['has_introduction'] else '❌'}")

        if completeness["missing_required"]:
            lines.append(f"Missing Required: {', '.join(completeness['missing_required'])}")
        if completeness["missing_recommended"]:
            lines.append(f"Missing Recommended: {', '.join(completeness['missing_recommended'])}")

        lines.append("=" * 60)
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Thesis Structure Mapper (Markdown / LaTeX)")
    parser.add_argument("path", help=".md/.tex file or thesis directory")
    parser.add_argument("--json", "-j", action="store_true", help="Output in JSON format")
    parser.add_argument(
        "--detect-template", "-d", action="store_true", help="Only detect and report template type"
    )
    parser.add_argument("--order", "-o", action="store_true", help="Output processing order")

    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        print(f"[ERROR] Path not found: {args.path}", file=sys.stderr)
        sys.exit(1)

    mapper = ThesisStructureMapper(str(path))
    structure = mapper.map()

    if args.detect_template:
        template = mapper.template
        info = mapper.get_template_info()
        if template:
            print(f"Template: {template}")
            if info:
                print(f"Name: {info['name']}")
                print(f"Figure format: {info['figure_format']}")
        else:
            print("Template: Not detected (Markdown project or generic)")
        sys.exit(0)

    if args.order:
        order = mapper.get_processing_order()
        print("Recommended processing order:")
        for i, f in enumerate(order, 1):
            print(f"  {i}. {f}")
        sys.exit(0)

    if args.json:
        output = {
            "template": mapper.template,
            "template_info": mapper.get_template_info(),
            "structure": structure,
            "completeness": mapper.check_completeness(),
            "processing_order": mapper.get_processing_order(),
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(mapper.generate_tree())


if __name__ == "__main__":
    import io, os
    if os.name == "nt":
        for stream in (sys.stdout, sys.stderr):
            if hasattr(stream, "reconfigure"):
                stream.reconfigure(encoding="utf-8")
            elif not isinstance(stream, io.TextIOWrapper):
                pass  # already ok
    main()
