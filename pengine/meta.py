"""Problem-metadata parser. Reads the `---` frontmatter block in problems/pNN.md.

    ---
    id: p01
    category: joins
    difficulty: easy
    tracks: sql, pyspark
    ordered: false
    columns: emp_id, name, dept_id
    tables: employees, departments
    hint: Inner join drops unmatched rows on both sides.
    ---
    <prompt body...>
"""
from pathlib import Path

from . import config


def _split(v):
    return [x.strip() for x in v.split(",") if x.strip()]


def parse(path):
    text = Path(path).read_text()
    meta, body = {}, text
    if text.startswith("---"):
        _, fm, body = text.split("---", 2)
        for line in fm.strip().splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
    meta["tracks"] = _split(meta.get("tracks", "sql, pyspark"))
    meta["columns"] = _split(meta.get("columns", ""))
    meta["tables"] = _split(meta.get("tables", ""))
    meta["ordered"] = str(meta.get("ordered", "false")).lower() == "true"
    meta["prompt"] = body.strip()
    return meta


def get(pid):
    return parse(config.PROBLEMS_DIR / f"{pid}.md")


def all_ids():
    return sorted(p.stem for p in config.PROBLEMS_DIR.glob("p*.md"))


def all_meta():
    return [get(pid) for pid in all_ids()]
