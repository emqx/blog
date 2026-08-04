# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Scan every git-tracked text file for plain `http://` links.

Site audits flag this as "HTTPS pages linking to HTTP pages": when a published
post on an HTTPS page links to an http:// URL, browsers warn the reader about a
non-secure page, which costs us site authority and hurts the experience. This
catches those links in source before they ship. It is a content check for SEO,
not a security control.

Prints `file:line:column` for each match and exits with code 1 when any is found.

Usage:
    uv run .ci/check_http_links.py            # scan every git-tracked file
    uv run .ci/check_http_links.py zh en      # scan the given files / directories

A URL is reported only when it points at a real public host. Local addresses,
placeholder hostnames and services on an explicit port are left alone; see
`is_excluded` for the full list of rules.

To allow a single link, put `http-link-check-ignore` on the same line or on the
line right above it. In Markdown use an HTML comment:

    <!-- http-link-check-ignore -->
    [example](http://example.invalid/)
"""

import ipaddress
import os
import re
import subprocess
import sys
from pathlib import Path

# Hosts that must stay on http://, subdomains included.
EXCLUDED_HOSTS = (
    # XML namespace and JSON Schema identifiers. The http:// form is the
    # literal value defined by the spec, rewriting it changes its meaning.
    'json-schema.org',
    'schema.org',
    'w3.org',
    'xmlsoap.org',
    # Reserved for documentation and examples, RFC 2606 / RFC 6761.
    'example.com',
    'example.net',
    'example.org',
    # Sites with no https listener, each verified by a TLS handshake.
    # The MQTTX Web host was retired for being http-only; the post that links
    # to it is the announcement of that retirement, so the scheme is the point.
    'mqtt-client.emqx.com',
    # Port-80 WebSocket endpoint listed in a table of public broker addresses.
    'mqtt.eclipseprojects.io',
    # PropEr project site.
    'proper.softlab.ntua.gr',
    # Bogus links produced by an editor that auto-linkified plain text such as
    # a file name, a config key or an ordinary word. The target is not a
    # website; the surrounding sentence should drop the link instead of
    # switching it to https.
    'init.sh',
    'node.name',
    'root.sg',
    't1.id',
    'nginx-1.xxx',
    'frameworks.de',
    'xn--microsoft-8f4h.net',
    'xn--core-ec4c.net',
)

# Single-label suffixes reserved for local use, RFC 6761 / RFC 8375.
EXCLUDED_TLDS = ('localhost', 'local', 'internal', 'home.arpa', 'test', 'invalid', 'example')

# Files that are never checked.
EXCLUDED_PATHS = (
    '.ci/check_http_links.py',
)

# Binary and media extensions, plus .svg which only holds namespace URIs.
EXCLUDED_EXTENSIONS = frozenset((
    '.svg',
    '.png', '.jpg', '.jpeg', '.gif', '.webp', '.avif', '.ico', '.bmp',
    '.woff', '.woff2', '.ttf', '.otf', '.eot',
    '.mp3', '.mp4', '.webm', '.mov', '.wav',
    '.pdf', '.zip', '.gz', '.tgz', '.br',
))

IGNORE_MARKER = 'http-link-check-ignore'
# Delimiters that cannot appear inside a URL. Brackets are in the set so that
# markdown link syntax does not bleed into the match, which means bracketed
# IPv6 authorities need their own alternative. Optional `userinfo@` is matched
# ahead of both alternatives so that it can precede a bracketed authority. CJK
# punctuation, fullwidth brackets, kana and Han characters end a URL too,
# because Chinese and Japanese prose runs straight into one with no space.
URL_DELIMITERS = r'[^\s"\'`<>()\[\]{},;\\|　-〿぀-ヿ㐀-䶿一-鿿＀-￯]'
URL_RE = re.compile(
    rf'http://(?:{URL_DELIMITERS}*@)?'
    rf'(?:\[[0-9a-f:.]+\]{URL_DELIMITERS}*|{URL_DELIMITERS}+)',
    re.IGNORECASE,
)
TRAILING_PUNCTUATION = '.,:;!?'
# Shell variables and format specifiers used in place of a real hostname.
PLACEHOLDER_RE = re.compile(r'[$%{}<>*]')


def git_output(*args: str, cwd: str | Path | None = None) -> str:
    """Run a git command and return its stdout."""
    return subprocess.run(
        ('git', *args),
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    ).stdout


def parse_authority(url: str) -> tuple[str, str]:
    """Split host and port out of a URL, handling user:pass@host and [::1]:8080."""
    authority = re.split(r'[/?#]', url[len('http://'):], maxsplit=1)[0]
    if '@' in authority:
        authority = authority.rsplit('@', 1)[1]
    # A sentence-ending period that markdown swallowed into the link target.
    authority = authority.rstrip('.')

    if authority.startswith('['):
        host, sep, rest = authority.partition(']')
        if not sep:
            return authority, ''
        return host + sep, rest[1:] if rest.startswith(':') else ''

    host, sep, port = authority.rpartition(':')
    if sep and port.isdigit():
        return host, port
    return authority, ''


def ip_literal(host: str) -> ipaddress.IPv4Address | ipaddress.IPv6Address | None:
    """Return the address when the host is an IP literal, otherwise None."""
    try:
        return ipaddress.ip_address(host.strip('[]'))
    except ValueError:
        return None


def is_excluded(url: str) -> bool:
    """Return True when the URL is allowed to stay on http://."""
    host, port = parse_authority(url)
    if not host:
        # Nothing that looks like a host, so nothing a reader can click. This
        # check exists to catch http:// links in copy, not to reject malformed
        # input, so leave these alone rather than report noise.
        return True

    # Any explicit port. A public web page is served on the default port, so a
    # URL that spells one out points at a dev server, an internal service or a
    # protocol endpoint such as a WebSocket listener.
    if port:
        return True

    host = host.lower().rstrip('.')

    # A hostname built from a shell variable or a printf placeholder.
    if PLACEHOLDER_RE.search(host):
        return True

    # Loopback, link-local, private and documentation addresses. Checked before
    # the single-label rule below, which an IPv6 literal would otherwise trip.
    address = ip_literal(host)
    if address is not None:
        return not address.is_global

    # A single-label name is not a public domain: localhost, a container name,
    # or a placeholder such as `yourhost` or `broker_host`.
    if '.' not in host:
        return True

    if any(host == tld or host.endswith(f'.{tld}') for tld in EXCLUDED_TLDS):
        return True

    return any(host == excluded or host.endswith(f'.{excluded}') for excluded in EXCLUDED_HOSTS)


def list_tracked_files(repo_root: Path) -> list[str]:
    """List every git-tracked file that takes part in the scan."""
    entries = git_output('ls-files', '-z', cwd=repo_root).split('\0')
    return sorted(entry for entry in entries if entry and is_scannable(entry))


def is_scannable(name: str) -> bool:
    """Return True when a path is neither excluded nor a binary/media file."""
    return (
        name not in EXCLUDED_PATHS
        and os.path.splitext(name)[1].lower() not in EXCLUDED_EXTENSIONS
    )


def collect_files(repo_root: Path, args: list[str]) -> list[str]:
    """Resolve command-line arguments to repo-relative paths, recursing into directories."""
    if not args:
        return list_tracked_files(repo_root)

    names: set[str] = set()
    for arg in args:
        path = Path(arg)
        candidates = sorted(p for p in path.rglob('*') if p.is_file()) if path.is_dir() else [path]
        for candidate in candidates:
            name = os.path.relpath(candidate.resolve(), repo_root)
            if is_scannable(name):
                names.add(name)
    return sorted(names)


def read_text_file(path: Path) -> str | None:
    """Read a text file, returning None for directories, submodules and binaries."""
    if not path.is_file():
        return None

    data = path.read_bytes()
    if b'\0' in data[:8192]:
        return None
    return data.decode('utf-8', errors='replace')


def scan_file(repo_root: Path, name: str) -> tuple[list[tuple[str, int, int, str]], int]:
    """Scan one file and return (findings, number of allowed matches)."""
    content = read_text_file(repo_root / name)
    # URI schemes are case-insensitive, so this fast path has to be too.
    if content is None or 'http://' not in content.lower():
        return [], 0

    lines = content.splitlines()
    findings: list[tuple[str, int, int, str]] = []
    allowed = 0

    for index, line in enumerate(lines):
        suppressed = IGNORE_MARKER in line or (index > 0 and IGNORE_MARKER in lines[index - 1])
        for match in URL_RE.finditer(line):
            url = match.group().rstrip(TRAILING_PUNCTUATION)
            if suppressed or is_excluded(url):
                allowed += 1
                continue
            findings.append((name, index + 1, match.start() + 1, url))

    return findings, allowed


def main() -> int:
    repo_root = Path(git_output('rev-parse', '--show-toplevel').strip())
    files = collect_files(repo_root, sys.argv[1:])

    findings: list[tuple[str, int, int, str]] = []
    allowed_count = 0
    for name in files:
        file_findings, file_allowed = scan_file(repo_root, name)
        findings.extend(file_findings)
        allowed_count += file_allowed

    if not findings:
        print(f'No http:// links found. Scanned {len(files)} files, '
              f'{allowed_count} matches allowed by the exclusion rules.')
        return 0

    file_count = len({name for name, _, _, _ in findings})
    link_label = 'link' if len(findings) == 1 else 'links'
    file_label = 'file' if file_count == 1 else 'files'
    print(f'Found {len(findings)} http:// {link_label} in {file_count} {file_label}:\n',
          file=sys.stderr)

    is_ci = os.environ.get('GITHUB_ACTIONS') == 'true'
    for name, line, column, url in findings:
        print(f'  {name}:{line}:{column}  {url}', file=sys.stderr)
        if is_ci:
            print(f'::error file={name},line={line},col={column}::Use https:// instead of {url}')

    print(
        f'\nUse https:// instead. If a link genuinely cannot use https, add its host to '
        f'EXCLUDED_HOSTS in .ci/check_http_links.py, or put `{IGNORE_MARKER}` in an HTML '
        f'comment on the line above it.',
        file=sys.stderr,
    )
    return 1


if __name__ == '__main__':
    sys.exit(main())
