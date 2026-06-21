"""Cheat sheets: static Markdown references under cheatsheets/, rendered to HTML.

No grading - pure reference content. Title is the first H1 in the file (or the
slug). Ordering follows a leading 'NN-' number in the filename when present.
"""
import re

import markdown

from . import config

_MD_EXT = ["fenced_code", "tables", "toc", "sane_lists"]


def _title(text, slug):
    m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    return m.group(1).strip() if m else slug


def _slug(path):
    # "01-sql-joins.md" -> "sql-joins"
    return re.sub(r"^\d+-", "", path.stem)


def list_sheets():
    if not config.CHEATS_DIR.exists():
        return []
    out = []
    for p in sorted(config.CHEATS_DIR.glob("*.md")):
        out.append({"slug": _slug(p), "title": _title(p.read_text(), _slug(p))})
    return out


def _path_for(slug):
    for p in config.CHEATS_DIR.glob("*.md"):
        if _slug(p) == slug:
            return p
    return None


def render(slug):
    p = _path_for(slug)
    if p is None:
        return None
    text = p.read_text()
    html = markdown.markdown(text, extensions=_MD_EXT)
    return {"slug": slug, "title": _title(text, slug), "html": html}
