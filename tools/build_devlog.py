#!/usr/bin/env python3
"""Render devlog.md into devlog.html.

devlog.md is the source of truth for the dev log's metrics band and its
entries. This script writes those two regions of devlog.html and touches
nothing else, so the page keeps its inline styles and stays a single
self-contained file that opens from disk.

Standard library only, no build tooling, no third-party parser. The
markdown accepted here is the small subset the log actually uses, not
markdown in general:

    # Metrics
    - 137 | Tests, all offline

    # Entries
    ## 0.19.0 | Monday Aug 17          version (or phase name) | date
    ### Headline for the entry
    > Pull quote, optional
    > -- who said it
    A paragraph, optional.
    - **Lead in bold.** Then the note.
    - [ok] **Verdict tag** instead of a bold lead. [bad] also works.

Inline: **bold** and *italic*. Nothing else, deliberately.

Usage:
    python3 tools/build_devlog.py            rewrite devlog.html
    python3 tools/build_devlog.py --check    exit 1 if it is out of date
"""
from __future__ import annotations

import html
import re
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "devlog.md"
PAGE = ROOT / "devlog.html"

METRICS_BEGIN = "<!-- build_devlog: metrics begin -->"
METRICS_END = "<!-- build_devlog: metrics end -->"
ENTRIES_BEGIN = "<!-- build_devlog: entries begin -->"
ENTRIES_END = "<!-- build_devlog: entries end -->"

WRAP = 76


class SourceError(SystemExit):
    def __init__(self, line_no: int, message: str) -> None:
        super().__init__(f"devlog.md line {line_no}: {message}")


def inline(text: str) -> str:
    """Escape, then apply the two inline marks. Escaping first means a
    stray angle bracket in the prose can never become markup."""
    out = html.escape(text, quote=False)
    out = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", out, flags=re.S)
    out = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<i>\1</i>", out, flags=re.S)
    if "**" in out:
        raise SystemExit(f"unclosed bold marker in: {text[:60]}")
    return out


def fill(text: str, indent: str) -> str:
    return textwrap.fill(
        text,
        width=WRAP,
        initial_indent=indent,
        subsequent_indent=indent,
        break_long_words=False,
        break_on_hyphens=False,
    )


def parse(source: str) -> tuple[list[tuple[str, str]], list[dict]]:
    metrics: list[tuple[str, str]] = []
    entries: list[dict] = []
    section: str | None = None
    entry: dict | None = None
    para: list[str] = []
    quote: list[str] = []
    note: list[str] = []

    def close_para() -> None:
        nonlocal para
        if para and entry is not None:
            entry["paragraphs"].append(" ".join(para))
        para = []

    def close_note() -> None:
        nonlocal note
        if note and entry is not None:
            entry["notes"].append(" ".join(note))
        note = []

    def close_quote() -> None:
        nonlocal quote
        if quote and entry is not None:
            who = None
            body = list(quote)
            if body and body[-1].startswith("-- "):
                who = body.pop()[3:].strip()
            entry["quote"] = (" ".join(body), who)
        quote = []

    for n, raw in enumerate(source.splitlines(), 1):
        line = raw.rstrip()
        stripped = line.strip()

        if stripped.startswith("# "):
            close_para(); close_note(); close_quote()
            heading = stripped[2:].strip().lower()
            if heading not in ("metrics", "entries"):
                raise SourceError(n, f'unknown section "{stripped[2:].strip()}"')
            section = heading
            continue

        if section is None:
            if stripped:
                raise SourceError(n, "content before the first # section heading")
            continue

        if section == "metrics":
            if not stripped:
                continue
            if not stripped.startswith("- "):
                raise SourceError(n, "metrics lines must start with '- '")
            if "|" not in stripped:
                raise SourceError(n, "metrics need 'value | label'")
            value, label = stripped[2:].split("|", 1)
            metrics.append((value.strip(), label.strip()))
            continue

        if stripped.startswith("## "):
            close_para(); close_note(); close_quote()
            if "|" not in stripped:
                raise SourceError(n, "entry heading needs 'version | date'")
            version, date = stripped[3:].split("|", 1)
            entry = {
                "version": version.strip(),
                "date": date.strip(),
                "headline": None,
                "quote": None,
                "paragraphs": [],
                "notes": [],
            }
            entries.append(entry)
            continue

        if entry is None:
            if stripped:
                raise SourceError(n, "content before the first ## entry heading")
            continue

        if stripped.startswith("### "):
            close_para(); close_note(); close_quote()
            if entry["headline"] is not None:
                raise SourceError(n, "entry already has a headline")
            entry["headline"] = stripped[4:].strip()
            continue

        if stripped.startswith(">"):
            close_para(); close_note()
            quote.append(stripped[1:].strip())
            continue

        if stripped.startswith("- "):
            close_para(); close_quote(); close_note()
            note.append(stripped[2:])
            continue

        if not stripped:
            close_para(); close_note(); close_quote()
            continue

        # A continuation line: indented under a note, otherwise prose.
        if note:
            note.append(stripped)
        else:
            close_quote()
            para.append(stripped)

    close_para(); close_note(); close_quote()

    for i, e in enumerate(entries, 1):
        if not e["headline"]:
            raise SystemExit(f"entry {i} ({e['version']}) has no ### headline")
    return metrics, entries


def render_metrics(metrics: list[tuple[str, str]]) -> str:
    out = []
    for value, label in metrics:
        out.append('    <div class="metric">')
        out.append(f'      <span class="v num">{inline(value)}</span>')
        out.append(f'      <span class="k mono">{inline(label)}</span>')
        out.append("    </div>")
    return "\n".join(out)


def render_note(text: str) -> str:
    """A note is one <li>. It may open with [ok] or [bad] plus a bold lead,
    which becomes a verdict tag instead of a plain bold run."""
    tag = re.match(r"\[(ok|bad)\]\s*\*\*(.+?)\*\*\s*(.*)$", text, flags=re.S)
    if tag:
        kind, lead, rest = tag.groups()
        head = f'<span class="tag {kind}">{inline(lead)}</span>'
        body = f"{head} {inline(rest)}" if rest.strip() else head
    else:
        body = inline(text)
    wrapped = fill(body, "          ").lstrip()
    lines = wrapped.split("\n")
    if len(lines) == 1:
        return f"        <li>{lines[0]}</li>"
    return "        <li>" + lines[0] + "\n" + "\n".join(lines[1:]) + "</li>"


def render_entries(entries: list[dict]) -> str:
    out = []
    for e in entries:
        kind = "num" if e["version"][:1].isdigit() else "word"
        out.append('  <article class="entry">')
        out.append('    <div class="when">')
        out.append(f'      <span class="ver {kind}">{inline(e["version"])}</span>')
        out.append(f'      <span class="date mono">{inline(e["date"])}</span>')
        out.append("    </div>")
        out.append("    <div>")
        out.append(f'      <h2 class="serif">{inline(e["headline"])}</h2>')

        if e["quote"]:
            text, who = e["quote"]
            out.append('      <div class="quote">')
            out.append(fill(inline(text), "        "))
            if who:
                out.append(f'        <span class="who">{inline(who)}</span>')
            out.append("      </div>")

        if e["paragraphs"]:
            out.append('      <div class="body">')
            for p in e["paragraphs"]:
                out.append("        <p>")
                out.append(fill(inline(p), "          "))
                out.append("        </p>")
            out.append("      </div>")

        if e["notes"]:
            out.append('      <ul class="notes">')
            for note in e["notes"]:
                out.append(render_note(note))
            out.append("      </ul>")

        out.append("    </div>")
        out.append("  </article>")
        out.append("")
    return "\n".join(out).rstrip("\n")


def splice(page: str, begin: str, end: str, block: str) -> str:
    i, j = page.find(begin), page.find(end)
    if i < 0 or j < 0:
        raise SystemExit(f"markers missing from devlog.html: {begin}")
    return page[: i + len(begin)] + "\n" + block + "\n" + page[j:]


def main() -> int:
    check = "--check" in sys.argv[1:]
    metrics, entries = parse(SOURCE.read_text(encoding="utf-8"))
    page = PAGE.read_text(encoding="utf-8")
    built = splice(page, METRICS_BEGIN, METRICS_END, render_metrics(metrics))
    built = splice(built, ENTRIES_BEGIN, ENTRIES_END, render_entries(entries))

    if check:
        if built != page:
            print("devlog.html is out of date; run python3 tools/build_devlog.py")
            return 1
        print(f"devlog.html is current: {len(entries)} entries, {len(metrics)} metrics")
        return 0

    if built == page:
        print(f"devlog.html already current: {len(entries)} entries")
        return 0
    PAGE.write_text(built, encoding="utf-8")
    print(f"devlog.html written: {len(entries)} entries, {len(metrics)} metrics")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
