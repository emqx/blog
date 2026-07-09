# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Check that blog Markdown files use a well-formed heading hierarchy.

Rules:
1. The body must not contain a level-1 heading (# ).
2. Heading levels must not skip a level; they may only deepen one step at
   a time, e.g. 2 3 4 2 is valid while 2 4 is not.
3. Heading formatting: exactly one space after the '#' marks, no missing
   space, and no leading indentation before the '#'.
4. README.md / README-JA.md / README-ZH.md are skipped.
"""

import re
import sys
from pathlib import Path

SKIP_FILES = {'README.md', 'README-JA.md', 'README-ZH.md'}

# ATX heading: up to 3 leading spaces, and '#' must be followed by a space
# or the end of the line. Used for the heading-level checks.
HEADING_RE = re.compile(r'^ {0,3}(#{1,6})(?:\s.*)?$')
# A line that looks like an ATX heading (1-6 '#' not followed by a 7th),
# with optional leading whitespace. Used for the formatting checks.
ATX_FORMAT_RE = re.compile(r'^(\s*)(#{1,6})(?!#)(.*)$')
# Code fence: ``` or ~~~, capturing the fence characters and the info string.
FENCE_RE = re.compile(r'^ {0,3}((`{3,})|(~{3,}))\s*(.*)$')


def scan_file(lines):
    """Scan the file once, skipping fenced code blocks.

    Fences follow CommonMark rules: a closing fence carries no info string
    and is no shorter than the opening fence; otherwise the line counts as
    ordinary content inside the fence.

    Returns (headings, format_issues) where headings is a list of
    (line_no, level, text) for well-formed ATX headings and format_issues
    is a list of (line_no, message).
    """
    headings = []
    format_issues = []
    fence_marker = None  # opening fence char ('`' or '~'); None when outside a fence
    fence_len = 0  # number of fence characters in the opening fence
    for line_no, line in enumerate(lines, start=1):
        fence_match = FENCE_RE.match(line)
        if fence_match:
            fence_str = fence_match.group(1)
            marker = fence_str[0]
            info = fence_match.group(4)
            if fence_marker is None:
                # Opening fence; an info string is allowed (e.g. ```shell).
                fence_marker = marker
                fence_len = len(fence_str)
                continue
            # Inside a fence: only close on the same char, sufficient length,
            # and no info string.
            if marker == fence_marker and len(fence_str) >= fence_len and not info:
                fence_marker = None
                fence_len = 0
            continue
        if fence_marker is not None:
            continue

        heading_match = HEADING_RE.match(line)
        if heading_match:
            level = len(heading_match.group(1))
            headings.append((line_no, level, line.strip()))

        format_issues.extend(check_heading_format(line_no, line))
    return headings, format_issues


def check_heading_format(line_no, line):
    """Return formatting issues for a single heading-like line."""
    match = ATX_FORMAT_RE.match(line)
    if not match:
        return []
    indent, hashes, rest = match.group(1), match.group(2), match.group(3)
    # A tab or 4+ leading spaces makes it an indented code block, not a heading.
    if '\t' in indent or len(indent) > 3:
        return []

    issues = []
    if indent:
        issues.append(
            (line_no, f'heading not at line start ({len(indent)} leading '
                      f'space(s)) -> {line.strip()}')
        )
    content = rest.lstrip(' \t')
    if content:
        spaces = rest[:len(rest) - len(content)]
        if spaces == '':
            issues.append(
                (line_no, f'missing space after "{hashes}" -> {line.strip()}')
            )
        elif len(spaces) >= 2:
            issues.append(
                (line_no, f'multiple spaces after "{hashes}" -> {line.strip()}')
            )
    return issues


def check_file(path):
    """Check a single file and return a list of issue messages."""
    lines = path.read_text(encoding='utf-8').splitlines()
    headings, format_issues = scan_file(lines)
    issues = []  # (line_no, message)

    # Rule 1: the body must not contain a level-1 heading.
    for line_no, level, text in headings:
        if level == 1:
            issues.append((line_no, f'level-1 heading found -> {text}'))

    # Rule 2: no skipped levels. The first body heading should be h2, and
    # each deepening step may only add one level.
    prev_level = 1  # implicit title level (h1) used as the baseline
    seen_heading = False
    for line_no, level, text in headings:
        if level == 1:
            # Level-1 headings are handled by rule 1; do not double-count
            # them as a skip here.
            prev_level = level
            seen_heading = True
            continue
        if level > prev_level + 1:
            if not seen_heading:
                issues.append(
                    (line_no, f'first body heading should be h2, got h{level} '
                              f'(skipped h2) -> {text}')
                )
            else:
                issues.append(
                    (line_no, f'heading jumps from h{prev_level} to h{level} '
                              f'-> {text}')
                )
        prev_level = level
        seen_heading = True

    # Rule 3: heading formatting (spacing / indentation).
    issues.extend(format_issues)

    issues.sort(key=lambda item: item[0])
    return [f'  line {line_no}: {message}' for line_no, message in issues]


def collect_md_files(paths):
    """Collect the Markdown files to scan from the command-line arguments.

    An argument may be a directory (scanned recursively) or a single .md
    file; with no arguments the current directory is scanned.
    """
    md_files = []
    for arg in paths:
        path = Path(arg)
        if path.is_dir():
            md_files.extend(
                p for p in path.rglob('*.md') if p.name not in SKIP_FILES
            )
        elif path.suffix == '.md' and path.name not in SKIP_FILES:
            md_files.append(path)
    return sorted(set(md_files))


def main():
    args = sys.argv[1:] if len(sys.argv) > 1 else ['.']
    md_files = collect_md_files(args)

    bad_files = 0
    for path in md_files:
        issues = check_file(path)
        if issues:
            bad_files += 1
            print(f'{path}')
            for issue in issues:
                print(issue)

    print('-' * 60)
    print(f'Scanned {len(md_files)} file(s), {bad_files} with issues.')
    return 1 if bad_files else 0


if __name__ == '__main__':
    sys.exit(main())
