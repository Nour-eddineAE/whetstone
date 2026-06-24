"""Access to answer files, reference solutions, and hints.

answers/ stay the single source of truth: both the CLI and the web app read and
write through here, so they can never grade different bytes.
"""
import re

from . import config, meta

# Matches import lines the grader injects automatically (pyspark.* + typing).
# Stripped from pyspark answers before displaying them in the editor so the
# user sees only their logic, not boilerplate.
_MANAGED_IMPORT_RE = re.compile(
    r"^\s*(from\s+pyspark\b|import\s+pyspark\b|from\s+typing\s+import\b)"
)


def strip_pyspark_imports(code: str) -> str:
    """Remove pyspark/typing import lines; drop leading blank lines left behind."""
    lines = code.split("\n")
    kept = [l for l in lines if not _MANAGED_IMPORT_RE.match(l)]
    while kept and not kept[0].strip():
        kept.pop(0)
    return "\n".join(kept)


def track_file(pid, track, ref=False):
    """Path to a problem's code file. ref=True -> reference under solutions/."""
    root = config.SOLUTIONS_DIR if ref else config.ANSWERS_DIR
    return root / track / f"{pid}.{config.EXT[track]}"


def read_answer(pid, track):
    f = track_file(pid, track)
    return f.read_text() if f.exists() else ""


def write_answer(pid, track, text):
    f = track_file(pid, track)
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(text)
    return f


def read_solution(pid, track):
    f = track_file(pid, track, ref=True)
    return f.read_text() if f.exists() else "(no reference for this track)"


def get_hint(pid, track=None):
    """Track-specific hint (hint_sql / hint_pyspark) when present, else the
    generic `hint`."""
    m = meta.get(pid)
    if track and m.get(f"hint_{track}"):
        return m[f"hint_{track}"]
    return m.get("hint", "(no hint)")
