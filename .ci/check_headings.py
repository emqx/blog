# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Check that blog Markdown files use a well-formed heading hierarchy.

Rules:
1. The body must not contain a level-1 heading (# ).
2. Heading levels must not skip a level; they may only deepen one step at
   a time, e.g. 2 3 4 2 is valid while 2 4 is not.
3. README.md / README-JA.md / README-ZH.md are skipped.
"""

import re
import sys
from pathlib import Path

SKIP_FILES = {'README.md', 'README-JA.md', 'README-ZH.md'}

# ATX heading: up to 3 leading spaces, and '#' must be followed by a space
# or the end of the line.
HEADING_RE = re.compile(r'^ {0,3}(#{1,6})(?:\s.*)?$')
# Code fence: ``` or ~~~, capturing the fence characters and the info string.
FENCE_RE = re.compile(r'^ {0,3}((`{3,})|(~{3,}))\s*(.*)$')


def extract_headings(lines):
    """Return the headings in the body, skipping fenced code blocks.

    Fences follow CommonMark rules: a closing fence carries no info string
    and is no shorter than the opening fence; otherwise the line counts as
    ordinary content inside the fence. Each item is (line_no, level, text).
    """
    headings = []
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
    return headings


def check_file(path):
    """Check a single file and return a list of issue messages."""
    lines = path.read_text(encoding='utf-8').splitlines()
    headings = extract_headings(lines)
    issues = []

    # Rule 1: the body must not contain a level-1 heading.
    for line_no, level, text in headings:
        if level == 1:
            issues.append(f'  line {line_no}: level-1 heading found -> {text}')

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
                    f'  line {line_no}: first body heading should be h2, '
                    f'got h{level} (skipped h2) -> {text}'
                )
            else:
                issues.append(
                    f'  line {line_no}: heading jumps from h{prev_level} '
                    f'to h{level} -> {text}'
                )
        prev_level = level
        seen_heading = True

    return issues


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
