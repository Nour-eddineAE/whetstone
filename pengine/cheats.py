"""Cheat sheets: static Markdown references under cheatsheets/, rendered to HTML.

No grading - pure reference content. Title is the first H1 in the file (or the
slug). Ordering follows a leading 'NN-' number in the filename when present.
Subject is derived from the slug prefix so the UI can group sheets.
"""
import re

import markdown

from . import config

_MD_EXT = ["fenced_code", "tables", "toc", "sane_lists"]

# Map slug prefix -> display subject name. Add new prefixes here as content grows.
_SUBJECT_MAP = {
    "sql":       "SQL",
    "pyspark":   "PySpark",
    "java":      "Java",
    "spring":    "Spring",
    "canonical": "Patterns",
    "interview": "Interview",
}
_SUBJECT_ORDER = list(_SUBJECT_MAP.values())


def _title(text, slug):
    m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    return m.group(1).strip() if m else slug


def _slug(path):
    # "01-sql-joins.md" -> "sql-joins"
    return re.sub(r"^\d+-", "", path.stem)


def _subject(slug):
    prefix = slug.split("-")[0]
    return _SUBJECT_MAP.get(prefix, prefix.title())


def list_sheets():
    if not config.CHEATS_DIR.exists():
        return []
    out = []
    for p in sorted(config.CHEATS_DIR.glob("*.md")):
        slug = _slug(p)
        out.append({"slug": slug, "title": _title(p.read_text(), slug), "subject": _subject(slug)})

    def _key(s):
        subj = s["subject"]
        i = _SUBJECT_ORDER.index(subj) if subj in _SUBJECT_ORDER else 99
        return (i, s["slug"])

    return sorted(out, key=_key)


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
