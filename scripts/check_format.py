#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Format Checker for Chinese Thesis (Markdown / LaTeX / Typst)

\u4f18\u5148\u68c0\u67e5\u6700\u8868\u9762\u7684\u9519\u8bef\uff1a\u9519\u522b\u5b57\u3001\u6807\u70b9\u3001\u683c\u5f0f\u3002

\u68c0\u67e5\u4f18\u5148\u7ea7:
  P0 - \u9519\u522b\u5b57 (typo): \u5b66\u672f\u8bba\u6587\u5e38\u89c1\u9519\u522b\u5b57\u3001\u5f62\u8fd1\u5b57\u6df7\u6dc6
  P1 - \u6807\u70b9 (punctuation): \u4e2d\u82f1\u6807\u70b9\u6df7\u7528\u3001\u8fde\u7eed\u6807\u70b9\u3001\u62ec\u53f7/\u5f15\u53f7\u4e0d\u914d\u5bf9\u3001\u53e5\u672b\u6807\u70b9
  P2 - \u683c\u5f0f (format): \u6807\u9898\u5c42\u7ea7\u8df3\u8dc3\u3001\u7a7a\u884c\u7f3a\u5931\u3001\u5f15\u7528\u683c\u5f0f\u3001\u6570\u5b66\u516c\u5f0f
  P3 - \u98ce\u683c (style): \u53e3\u8bed\u5316\u8868\u8fbe\u3001\u7a7a\u683c\u89c4\u8303

Usage:
    uv run python check_format.py thesis.md
    uv run python check_format.py thesis.md --strict
    uv run python check_format.py thesis_dir/ --json
"""

import argparse
import json
import re
import sys
from pathlib import Path

try:
    from parsers import get_parser
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    from parsers import get_parser


# P0: \u9519\u522b\u5b57 \u2014 \u5b66\u672f\u8bba\u6587\u4e2d\u6700\u5e38\u89c1\u7684\u5f62\u8fd1\u5b57/\u97f3\u8fd1\u5b57\u6df7\u6dc6
# \u6bcf\u6761\u89c4\u5219: (pattern, correct, description)
TYPO_RULES = [
    # \u5f62\u8fd1\u5b57\u6df7\u6dc6
    ("\u5df1\u7ecf", "\u5df2\u7ecf", "\u5f62\u8fd1\u5b57\uff1a\u5df1\u2192\u5df2"),
    ("\u4ee5\u7ecf", "\u5df2\u7ecf", "\u97f3\u8fd1\u5b57\uff1a\u4ee5\u2192\u5df2"),
    ("\u505a\u4e3a", "\u4f5c\u4e3a", "\u5e38\u89c1\u9519\u522b\u5b57\uff1a\u505a\u2192\u4f5c"),
    ("\u5176\u5b83", "\u5176\u4ed6", "\u5b66\u672f\u89c4\u8303\u7528\u5176\u4ed6"),
    ("\u7cbe\u5178", "\u7ecf\u5178", "\u5f62\u8fd1\u5b57\uff1a\u7cbe\u2192\u7ecf"),
    ("\u66b4\u5149", "\u66dd\u5149", "\u5e38\u89c1\u9519\u522b\u5b57"),
    ("\u4faf\u9009", "\u5019\u9009", "\u5f62\u8fd1\u5b57\uff1a\u4faf\u2192\u5019"),
    ("\u4faf\u8865", "\u5019\u8865", "\u5f62\u8fd1\u5b57\uff1a\u4faf\u2192\u5019"),
    ("\u5e10\u53f7", "\u8d26\u53f7", "\u5f62\u8fd1\u5b57\uff1a\u5e10\u2192\u8d26"),
    ("\u4efd\u91cf", "\u5206\u91cf", "\u5e38\u89c1\u9519\u522b\u5b57"),
    ("\u5ea7\u6807", "\u5750\u6807", "\u5b66\u672f\u89c4\u8303\u7528\u5750\u6807"),
    ("\u4e13\u7814", "\u94bb\u7814", "\u97f3\u8fd1\u5b57\u6df7\u6dc6"),
    ("\u9898\u7eb2", "\u63d0\u7eb2", "\u97f3\u8fd1\u5b57\u6df7\u6dc6"),
    # \u6210\u8bed\u8bef\u7528
    ("\u957f\u671f\u4ee5\u5f80", "\u957f\u6b64\u4ee5\u5f80", "\u5e38\u89c1\u6210\u8bed\u8bef\u7528"),
    ("\u8feb\u4e0d\u6025\u5f85", "\u8feb\u4e0d\u53ca\u5f85", "\u5e38\u89c1\u6210\u8bed\u8bef\u7528"),
    ("\u4e00\u5982\u7ee7\u5f80", "\u4e00\u5982\u65e2\u5f80", "\u5e38\u89c1\u6210\u8bed\u8bef\u7528"),
    ("\u53d8\u6362\u83ab\u6d4b", "\u53d8\u5e7b\u83ab\u6d4b", "\u5e38\u89c1\u6210\u8bed\u8bef\u7528"),
    ("\u8d70\u5934\u65e0\u8def", "\u8d70\u6295\u65e0\u8def", "\u5e38\u89c1\u6210\u8bed\u8bef\u7528"),
    ("\u518d\u63a5\u518d\u5386", "\u518d\u63a5\u518d\u52b1", "\u5e38\u89c1\u6210\u8bed\u8bef\u7528"),
    ("\u6309\u6b65\u5c31\u73ed", "\u6309\u90e8\u5c31\u73ed", "\u5e38\u89c1\u6210\u8bed\u8bef\u7528"),
    ("\u9488\u8d2c\u65f6\u5f0a", "\u9488\u7824\u65f6\u5f0a", "\u5e38\u89c1\u6210\u8bed\u8bef\u7528"),
    # \u8d58\u4f59\u8868\u8fbe
    ("\u64c5\u957f\u4e8e", "\u64c5\u957f", "\u8d58\u4f59\uff1a\u53bb\u6389\u4e8e"),
    ("\u5927\u7ea6.{1,4}\u5de6\u53f3", "\u5927\u7ea6/\u5de6\u53f3", "\u5927\u7ea6\u548c\u5de6\u53f3\u8bed\u4e49\u91cd\u590d"),
    ("\u53ef\u4ee5\u80fd\u591f", "\u53ef\u4ee5/\u80fd\u591f", "\u91cd\u590d\u8868\u8fbe"),
    # \u7684\u5730\u5f97 \u2014 \u4fee\u9970\u52a8\u8bcd\u5e94\u7528\u5730
    ("\u8ba4\u771f\u7684(?=\u5b66\u4e60|\u7814\u7a76|\u5206\u6790|\u5de5\u4f5c|\u601d\u8003|\u6267\u884c|\u63a2\u8ba8)", "\u8ba4\u771f\u5730", "\u7684\u2192\u5730\uff0c\u4fee\u9970\u52a8\u8bcd\u7528\u5730"),
    ("\u4ed4\u7ec6\u7684(?=\u68c0\u67e5|\u5206\u6790|\u89c2\u5bdf|\u7814\u7a76|\u67e5\u770b|\u9605\u8bfb)", "\u4ed4\u7ec6\u5730", "\u7684\u2192\u5730\uff0c\u4fee\u9970\u52a8\u8bcd\u7528\u5730"),
    ("\u6df1\u5165\u7684(?=\u7814\u7a76|\u5206\u6790|\u63a2\u8ba8|\u8ba8\u8bba|\u7406\u89e3|\u5b66\u4e60)", "\u6df1\u5165\u5730", "\u7684\u2192\u5730\uff0c\u4fee\u9970\u52a8\u8bcd\u7528\u5730"),
    ("\u7cfb\u7edf\u7684(?=\u5206\u6790|\u7814\u7a76|\u8ba8\u8bba|\u603b\u7ed3|\u8bbe\u8ba1|\u4f18\u5316)", "\u7cfb\u7edf\u5730", "\u7684\u2192\u5730\uff0c\u4fee\u9970\u52a8\u8bcd\u7528\u5730"),
    ("\u5168\u9762\u7684(?=\u5206\u6790|\u7814\u7a76|\u8ba8\u8bba|\u603b\u7ed3|\u68c0\u9a8c|\u8bc4\u4f30)", "\u5168\u9762\u5730", "\u7684\u2192\u5730\uff0c\u4fee\u9970\u52a8\u8bcd\u7528\u5730"),
    ("\u6709\u6548\u7684(?=\u89e3\u51b3|\u964d\u4f4e|\u63d0\u9ad8|\u6539\u5584|\u907f\u514d|\u5229\u7528)", "\u6709\u6548\u5730", "\u7684\u2192\u5730\uff0c\u4fee\u9970\u52a8\u8bcd\u7528\u5730"),
    ("\u51c6\u786e\u7684(?=\u63cf\u8ff0|\u53cd\u6620|\u9884\u6d4b|\u8ba1\u7b97|\u6d4b\u91cf|\u4f30\u8ba1)", "\u51c6\u786e\u5730", "\u7684\u2192\u5730\uff0c\u4fee\u9970\u52a8\u8bcd\u7528\u5730"),
    ("\u5feb\u901f\u7684(?=\u6536\u655b|\u589e\u957f|\u53d1\u5c55|\u5b8c\u6210|\u5b9e\u73b0)", "\u5feb\u901f\u5730", "\u7684\u2192\u5730\uff0c\u4fee\u9970\u52a8\u8bcd\u7528\u5730"),
    ("\u663e\u8457\u7684(?=\u63d0\u9ad8|\u6539\u5584|\u964d\u4f4e|\u4f18\u4e8e|\u589e\u52a0|\u51cf\u5c11)", "\u663e\u8457\u5730", "\u7684\u2192\u5730\uff0c\u4fee\u9970\u52a8\u8bcd\u7528\u5730"),
    ("\u5145\u5206\u7684(?=\u5229\u7528|\u8bf4\u660e|\u8bc1\u660e|\u4f53\u73b0|\u8003\u8651|\u53d1\u6325)", "\u5145\u5206\u5730", "\u7684\u2192\u5730\uff0c\u4fee\u9970\u52a8\u8bcd\u7528\u5730"),
]


# P1: \u6807\u70b9\u9519\u8bef - \u4f7f\u7528\u6b63\u5219\u5b57\u7b26\u7c7b\u6765\u907f\u514d\u5b57\u7b26\u4e32\u5f15\u53f7\u51b2\u7a81
PUNCTUATION_RULES = [
    # (name, pattern, message, severity)
    # \u4e2d\u82f1\u6807\u70b9\u6df7\u7528
    ("mixed_punct_after_cn",
     r"[\u4e00-\u9fff][,.:;!?()]+",
     "\u4e2d\u6587\u540e\u4f7f\u7528\u4e86\u82f1\u6587\u6807\u70b9", "error"),
    ("mixed_punct_before_cn",
     r"[,.:;!?][\u4e00-\u9fff]",
     "\u82f1\u6587\u6807\u70b9\u540e\u76f4\u63a5\u8ddf\u4e2d\u6587", "error"),
    # \u8fde\u7eed\u6807\u70b9
    ("consecutive_comma",
     r"[\uff0c,]{2,}",
     "\u8fde\u7eed\u9017\u53f7", "error"),
    ("consecutive_period",
     r"[\u3002.]{2,}",
     "\u8fde\u7eed\u53e5\u53f7", "error"),
    ("consecutive_cn_punct",
     r"[\uff0c\u3002\uff1b\uff1a\uff01\uff1f]{2}",
     "\u8fde\u7eed\u4e2d\u6587\u6807\u70b9", "warning"),
    # \u7a7a\u4e66\u540d\u53f7
    ("empty_book_mark",
     r"\u300a\u300b",
     "\u7a7a\u4e66\u540d\u53f7", "error"),
    # \u4e2d\u6587\u6807\u70b9\u524d\u591a\u4f59\u7a7a\u683c
    ("space_before_cn_punct",
     r"\s+[\uff0c\u3002\uff1b\uff1a\uff01\uff1f]",
     "\u4e2d\u6587\u6807\u70b9\u524d\u6709\u591a\u4f59\u7a7a\u683c", "warning"),
    # \u5168\u89d2\u82f1\u6587\u5b57\u6bcd/\u6570\u5b57
    ("fullwidth_alpha",
     r"[\uff21-\uff3a\uff41-\uff5a\uff10-\uff19]",
     "\u4f7f\u7528\u4e86\u5168\u89d2\u5b57\u6bcd/\u6570\u5b57\uff0c\u5e94\u4f7f\u7528\u534a\u89d2", "error"),
]


# P3: \u98ce\u683c\u95ee\u9898
STYLE_RULES = [
    ("oral_expression",
     r"(?<![a-zA-Z])(?:\u6211\u4eec|\u4f60\u4eec|\u54b1\u4eec|\u5f88\u591a|\u4e00\u4e9b|\u975e\u5e38|\u7279\u522b|\u592a\u591a|\u597d\u591a|\u631a\u597d)(?![a-zA-Z])",
     "\u5b66\u672f\u5199\u4f5c\u4e2d\u7684\u53e3\u8bed\u5316\u8868\u8fbe", "info"),
    ("subjective_pronoun",
     r"(?:\u6211\u89c9\u5f97|\u6211\u8ba4\u4e3a|\u6211\u60f3|\u6211\u4eec\u8ba4\u4e3a|\u53ef\u4ee5\u8bf4)",
     "\u5b66\u672f\u5199\u4f5c\u4e2d\u5e94\u907f\u514d\u4e3b\u89c2\u4ee3\u8bcd", "info"),
    ("exaggeration",
     r"(?:\u78be\u538b|\u9065\u9065\u9886\u5148|\u65e0\u4e0e\u4f26\u6bd4|\u5b8c\u7f8e|\u6700\u597d\u7684|\u9769\u547d\u6027|\u98a0\u8986\u6027)",
     "\u5b66\u672f\u5199\u4f5c\u4e2d\u5e94\u907f\u514d\u5938\u5f20\u8868\u8ff0", "warning"),
    ("cn_en_space_missing",
     r"[\u4e00-\u9fff][a-zA-Z]|[a-zA-Z][\u4e00-\u9fff]",
     "\u4e2d\u82f1\u6587\u4e4b\u95f4\u5efa\u8bae\u52a0\u7a7a\u683c", "info"),
]


class FormatChecker:
    """Format checker with Chinese thesis specific rules.

    \u68c0\u67e5\u4f18\u5148\u7ea7\uff1aP0 \u9519\u522b\u5b57 > P1 \u6807\u70b9 > P2 \u683c\u5f0f > P3 \u98ce\u683c
    """

    # \u6bb5\u843d\u672b\u5c3e\u5408\u6cd5\u7684\u4e2d\u6587\u6807\u70b9
    CN_END_PUNCTS = "\u3002\uff01\uff1f\uff1b\uff1a\u2026\u300d\u3011\uff09\u300b"

    def __init__(self, file_path: str):
        self.file_path = Path(file_path).resolve()
        self.parser = get_parser(file_path)

    def check(self, strict: bool = False) -> dict:
        """Run format checks in priority order."""
        try:
            content = self.file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            return {"status": "ERROR", "issues": [{"message": str(e)}], "total": 1,
                    "errors": 1, "warnings": 0, "info": 0}

        lines = content.split("\n")
        comment_prefix = self.parser.get_comment_prefix()

        # Track code blocks to skip
        in_code_block = False
        skip_lines = set()
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith("```"):
                in_code_block = not in_code_block
                skip_lines.add(i)
                continue
            if in_code_block:
                skip_lines.add(i)
            if stripped.startswith(comment_prefix):
                skip_lines.add(i)

        all_issues = []

        # P0: \u9519\u522b\u5b57
        all_issues.extend(self._check_typos(lines, skip_lines))
        # P1: \u6807\u70b9
        all_issues.extend(self._check_punctuation(lines, skip_lines))
        # P1: \u62ec\u53f7\u914d\u5bf9
        all_issues.extend(self._check_bracket_pairs(lines, skip_lines))
        # P1: \u6bb5\u672b\u6807\u70b9
        all_issues.extend(self._check_end_punct(lines, skip_lines))
        # P2: Markdown \u683c\u5f0f
        if str(self.file_path).lower().endswith(".md"):
            all_issues.extend(self._check_markdown_format(lines, skip_lines))
        # P3: \u98ce\u683c
        if strict:
            all_issues.extend(self._check_style(lines, skip_lines))

        # Sort by priority, then line
        priority_order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
        all_issues.sort(
            key=lambda x: (priority_order.get(x.get("priority", "P3"), 9), x.get("line", 0))
        )

        error_count = sum(1 for i in all_issues if i.get("severity") == "error")
        warn_count = sum(1 for i in all_issues if i.get("severity") == "warning")
        info_count = sum(1 for i in all_issues if i.get("severity") == "info")
        status = "FAIL" if error_count > 0 else ("WARNING" if all_issues else "PASS")

        return {
            "status": status,
            "issues": all_issues,
            "total": len(all_issues),
            "errors": error_count,
            "warnings": warn_count,
            "info": info_count,
        }

    def _clean_line(self, line: str) -> str:
        """Remove citations, math, URLs, links from line before checking punctuation."""
        cleaned = line
        cleaned = re.sub(r"\[@[^\]]+\]", "", cleaned)         # Pandoc citations
        cleaned = re.sub(r"\$\$[^$]*\$\$", "", cleaned)       # Display math
        cleaned = re.sub(r"\$[^$]+\$", "", cleaned)            # Inline math
        cleaned = re.sub(r"https?://\S+", "", cleaned)         # URLs
        cleaned = re.sub(r"!?\[[^\]]*\]\([^)]+\)", "", cleaned)  # Links/images
        cleaned = re.sub(r"\\cite\{[^}]+\}", "", cleaned)     # LaTeX cite
        return cleaned

    # P0
    def _check_typos(self, lines, skip_lines):
        issues = []
        for i, line in enumerate(lines, 1):
            if i in skip_lines:
                continue
            stripped = line.strip()
            if stripped.startswith("$$") or stripped.startswith("$"):
                continue
            for pattern, correct, desc in TYPO_RULES:
                for match in re.finditer(pattern, line):
                    suggestion = ""
                    if correct:
                        suggestion = " \u2192 " + correct
                    issues.append({
                        "priority": "P0",
                        "source": "typo",
                        "file": str(self.file_path.name),
                        "line": i,
                        "column": match.start() + 1,
                        "severity": "error",
                        "code": "typo",
                        "message": "\u7591\u4f3c\u9519\u522b\u5b57\uff1a" + match.group() + suggestion + "\uff08" + desc + "\uff09",
                        "matched": match.group(),
                    })
        return issues

    # P1
    def _check_punctuation(self, lines, skip_lines):
        issues = []
        for name, pattern, message, severity in PUNCTUATION_RULES:
            for i, line in enumerate(lines, 1):
                if i in skip_lines:
                    continue
                cleaned = self._clean_line(line)
                for match in re.finditer(pattern, cleaned):
                    issues.append({
                        "priority": "P1",
                        "source": "punctuation",
                        "file": str(self.file_path.name),
                        "line": i,
                        "column": match.start() + 1,
                        "severity": severity,
                        "code": name,
                        "message": message,
                        "matched": match.group(),
                    })
        return issues

    def _check_bracket_pairs(self, lines, skip_lines):
        """Check unmatched bracket/quote pairs per line."""
        issues = []
        pairs = [
            ("\uff08", "\uff09"),   # \uff08\uff09
            ("\u3010", "\u3011"),   # \u3010\u3011
            ("\u300a", "\u300b"),   # \u300a\u300b
            ("\u201c", "\u201d"),   # \u201c\u201d
            ("\u2018", "\u2019"),   # \u2018\u2019
        ]
        for i, line in enumerate(lines, 1):
            if i in skip_lines:
                continue
            for left, right in pairs:
                lc = line.count(left)
                rc = line.count(right)
                if lc != rc:
                    issues.append({
                        "priority": "P1",
                        "source": "punctuation",
                        "file": str(self.file_path.name),
                        "line": i,
                        "column": 1,
                        "severity": "warning",
                        "code": "unmatched_pair",
                        "message": left + right + "\u4e0d\u914d\u5bf9\uff08" + left + "\u00d7" + str(lc) + ", " + right + "\u00d7" + str(rc) + "\uff09",
                    })
        return issues

    def _check_end_punct(self, lines, skip_lines):
        """Check if Chinese paragraph ends without terminal punctuation."""
        issues = []
        total = len(lines)
        for i, line in enumerate(lines, 1):
            if i in skip_lines:
                continue
            stripped = line.rstrip()
            if not stripped:
                continue
            # Skip headings, lists, tables, images, math, block quotes
            if re.match(r"^(#{1,6}\s|[-*+]\s|\d+\.\s|\||!\[|\$\$|>)", stripped):
                continue
            cn_chars = len(re.findall(r"[\u4e00-\u9fff]", stripped))
            if cn_chars < 5:
                continue
            # Check if next line is blank (paragraph boundary)
            next_is_break = (i >= total) or (not lines[i].strip() if i < total else True)
            if next_is_break and stripped[-1] not in self.CN_END_PUNCTS:
                issues.append({
                    "priority": "P1",
                    "source": "punctuation",
                    "file": str(self.file_path.name),
                    "line": i,
                    "column": len(stripped),
                    "severity": "warning",
                    "code": "missing_end_punct",
                    "message": "\u6bb5\u843d\u672b\u5c3e\u7f3a\u5c11\u6807\u70b9\uff08\u672b\u5b57\u7b26\uff1a" + stripped[-1] + "\uff09",
                })
        return issues

    # P2
    def _check_markdown_format(self, lines, skip_lines):
        issues = []
        prev_level = 0
        for i, line in enumerate(lines, 1):
            if i in skip_lines:
                continue
            stripped = line.strip()
            match = re.match(r"^(#{1,6})\s+", stripped)
            if match:
                level = len(match.group(1))
                if prev_level > 0 and level > prev_level + 1:
                    issues.append({
                        "priority": "P2",
                        "source": "markdown_format",
                        "file": str(self.file_path.name),
                        "line": i,
                        "column": 1,
                        "severity": "warning",
                        "code": "heading_level_skip",
                        "message": "\u6807\u9898\u5c42\u7ea7\u8df3\u8dc3\uff1a\u4ece " + "#" * prev_level + " \u76f4\u63a5\u8df3\u5230 " + "#" * level,
                    })
                if i > 1 and i - 1 not in skip_lines and lines[i - 2].strip():
                    issues.append({
                        "priority": "P2",
                        "source": "markdown_format",
                        "file": str(self.file_path.name),
                        "line": i,
                        "column": 1,
                        "severity": "info",
                        "code": "missing_blank_before_heading",
                        "message": "\u6807\u9898\u524d\u7f3a\u5c11\u7a7a\u884c",
                    })
                prev_level = level

        # Pandoc citation spacing
        for i, line in enumerate(lines, 1):
            if i in skip_lines:
                continue
            for match in re.finditer(r"\[@[^\]]+\][\u4e00-\u9fff]", line):
                issues.append({
                    "priority": "P2",
                    "source": "markdown_format",
                    "file": str(self.file_path.name),
                    "line": i,
                    "column": match.start() + 1,
                    "severity": "info",
                    "code": "missing_space_after_cite",
                    "message": "Pandoc \u5f15\u7528 [@key] \u540e\u7f3a\u5c11\u7a7a\u683c",
                    "matched": match.group(),
                })
        return issues

    # P3
    def _check_style(self, lines, skip_lines):
        issues = []
        for name, pattern, message, severity in STYLE_RULES:
            for i, line in enumerate(lines, 1):
                if i in skip_lines:
                    continue
                for match in re.finditer(pattern, line):
                    issues.append({
                        "priority": "P3",
                        "source": "style",
                        "file": str(self.file_path.name),
                        "line": i,
                        "column": match.start() + 1,
                        "severity": severity,
                        "code": name,
                        "message": message,
                        "matched": match.group(),
                    })
        return issues

    # \u62a5\u544a
    def generate_report(self, result: dict) -> str:
        lines = []
        lines.append("=" * 60)
        lines.append("\u8bba\u6587\u683c\u5f0f\u68c0\u67e5\u62a5\u544a")
        lines.append("=" * 60)
        lines.append("\u6587\u4ef6: " + self.file_path.name)
        lines.append("\u72b6\u6001: " + result["status"])
        lines.append(
            "\u95ee\u9898\u603b\u6570: " + str(result["total"]) + "  "
            "(\u9519\u8bef: " + str(result.get("errors", 0)) + ", "
            "\u8b66\u544a: " + str(result.get("warnings", 0)) + ", "
            "\u63d0\u793a: " + str(result.get("info", 0)) + ")"
        )

        if not result["issues"]:
            lines.append("")
            lines.append("\u2705 \u672a\u53d1\u73b0\u8868\u9762\u683c\u5f0f\u95ee\u9898\u3002")
            lines.append("=" * 60)
            return "\n".join(lines)

        by_priority = {}
        for issue in result["issues"]:
            p = issue.get("priority", "P3")
            if p not in by_priority:
                by_priority[p] = []
            by_priority[p].append(issue)

        priority_labels = {
            "P0": "\U0001f534 P0 \u9519\u522b\u5b57",
            "P1": "\U0001f7e0 P1 \u6807\u70b9\u9519\u8bef",
            "P2": "\U0001f7e1 P2 \u683c\u5f0f\u95ee\u9898",
            "P3": "\U0001f535 P3 \u98ce\u683c\u5efa\u8bae",
        }

        for p in ["P0", "P1", "P2", "P3"]:
            if p not in by_priority:
                continue
            p_issues = by_priority[p]
            label = priority_labels.get(p, p)
            lines.append("")
            lines.append("\u2500" * 60)
            lines.append(label + "  (" + str(len(p_issues)) + " \u9879)")
            lines.append("\u2500" * 60)

            for issue in p_issues[:30]:
                sev = issue.get("severity", "info")
                icon = {"error": "\u2716", "warning": "\u26a0", "info": "\u2139"}.get(sev, "\u00b7")
                msg = issue["message"]
                matched = issue.get("matched", "")
                loc = "L" + str(issue["line"])
                if matched:
                    lines.append("  " + icon + " " + loc + ": " + msg + " \u2500 \u300c" + matched + "\u300d")
                else:
                    lines.append("  " + icon + " " + loc + ": " + msg)

            if len(p_issues) > 30:
                lines.append("  \u2026 \u8fd8\u6709 " + str(len(p_issues) - 30) + " \u9879")

        lines.append("")
        lines.append("=" * 60)
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="\u8bba\u6587\u683c\u5f0f\u68c0\u67e5 \u2014 \u9519\u522b\u5b57\u00b7\u6807\u70b9\u00b7\u683c\u5f0f\u00b7\u98ce\u683c\uff08\u652f\u6301 Markdown/LaTeX\uff09",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "\u68c0\u67e5\u4f18\u5148\u7ea7:\n"
            "  P0 - \u9519\u522b\u5b57     \u6700\u9ad8\u4f18\u5148\u7ea7\uff0c\u76f4\u63a5\u5f71\u54cd\u8bba\u6587\u8d28\u91cf\n"
            "  P1 - \u6807\u70b9\u9519\u8bef   \u4e2d\u82f1\u6807\u70b9\u6df7\u7528\u3001\u8fde\u7eed\u6807\u70b9\u3001\u62ec\u53f7\u4e0d\u914d\u5bf9\n"
            "  P2 - \u683c\u5f0f\u95ee\u9898   \u6807\u9898\u5c42\u7ea7\u8df3\u8dc3\u3001\u7a7a\u884c\u7f3a\u5931\uff08\u4ec5 Markdown\uff09\n"
            "  P3 - \u98ce\u683c\u5efa\u8bae   \u53e3\u8bed\u5316\u8868\u8fbe\u3001\u4e2d\u82f1\u6587\u7a7a\u683c\uff08\u9700 --strict\uff09"
        ),
    )
    parser.add_argument("path", help=".md/.tex \u6587\u4ef6\u6216\u76ee\u5f55")
    parser.add_argument("--strict", "-s", action="store_true",
                        help="\u542f\u7528\u4e25\u683c\u68c0\u67e5\uff08\u542b P3 \u98ce\u683c\u5efa\u8bae\uff09")
    parser.add_argument("--json", "-j", action="store_true", help="JSON \u683c\u5f0f\u8f93\u51fa")

    args = parser.parse_args()
    path = Path(args.path)

    if path.is_dir():
        files = sorted(set(list(path.rglob("*.md")) + list(path.rglob("*.tex"))))
    elif path.exists():
        files = [path]
    else:
        print("[ERROR] \u6587\u4ef6\u672a\u627e\u5230: " + args.path)
        sys.exit(1)

    all_results = {}
    has_errors = False
    total_issues = 0

    for f in sorted(files):
        checker = FormatChecker(str(f))
        result = checker.check(strict=args.strict)
        all_results[str(f)] = result
        total_issues += result["total"]
        if result["status"] == "FAIL":
            has_errors = True

        if not args.json:
            print(checker.generate_report(result))

    if len(files) > 1 and not args.json:
        print("")
        print("=" * 60)
        print("\u6c47\u603b: " + str(len(files)) + " \u4e2a\u6587\u4ef6\uff0c\u5171 " + str(total_issues) + " \u4e2a\u95ee\u9898")
        print("=" * 60)

    if args.json:
        print(json.dumps(all_results, indent=2, ensure_ascii=False))

    sys.exit(1 if has_errors else 0)


if __name__ == "__main__":
    import io, os
    if os.name == "nt":
        for stream in (sys.stdout, sys.stderr):
            if hasattr(stream, "reconfigure"):
                stream.reconfigure(encoding="utf-8")
    main()
