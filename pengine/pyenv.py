"""Python interpreter selection + Jedi-powered code completion.

The editor's PySpark autocomplete is env-aware: it introspects a chosen Python
interpreter's installed libraries (pyspark, pandas, ...) through Jedi, so you get
real module/class/function names, signatures, and types -- not just words from
the buffer. The selected interpreter is persisted in `.whetstone.json` at the
project root (gitignored), so it survives restarts.
"""
import json
import os
import sys
from pathlib import Path

from . import config

SETTINGS_FILE = config.ROOT / ".whetstone.json"

# Jedi Environments are expensive to build (they shell out to the interpreter),
# so cache them by executable path for the life of the process.
_env_cache = {}


# ---------------------------------------------------------------- settings ---
def load_settings():
    try:
        return json.loads(SETTINGS_FILE.read_text())
    except (FileNotFoundError, ValueError):
        return {}


def save_settings(data):
    SETTINGS_FILE.write_text(json.dumps(data, indent=2))


def current_interpreter():
    """Selected interpreter path, falling back to the one running the server."""
    return load_settings().get("interpreter") or sys.executable


def set_interpreter(path):
    """Persist the chosen interpreter. Returns the validated absolute path."""
    p = Path(path).expanduser()
    if not p.exists():
        raise FileNotFoundError(f"no such interpreter: {p}")
    data = load_settings()
    data["interpreter"] = str(p)
    save_settings(data)
    return str(p)


# ------------------------------------------------------------ discovery ------
def _conda_env_dirs():
    roots = [Path.home() / d for d in ("miniconda3", "anaconda3", ".conda")]
    for root in roots:
        envs = root / "envs"
        if envs.is_dir():
            for env in sorted(envs.iterdir()):
                exe = env / "bin" / "python"
                if exe.exists():
                    yield exe


def _version_of(exe):
    try:
        import jedi
        return jedi.create_environment(str(exe), safe=False).version_info
    except Exception:
        return None


def discover_environments():
    """Find candidate interpreters: system Pythons, conda envs, the running one.

    Deduped by resolved path. Each entry: {path, label, current}.
    """
    import jedi

    found = {}

    def add(exe, kind):
        try:
            real = str(Path(exe).resolve())
        except OSError:
            return
        if real in found:
            return
        found[real] = kind

    add(sys.executable, "running server")
    for e in _conda_env_dirs():
        add(e, "conda")
    try:
        for env in jedi.find_system_environments():
            add(env.executable, "system")
    except Exception:
        pass

    cur = str(Path(current_interpreter()).resolve())
    out = []
    for path, kind in found.items():
        name = Path(path).parent.parent.name  # env dir name (…/envs/general/bin/python)
        out.append({
            "path": path,
            "label": f"{name} ({kind})" if name not in ("", "/") else f"{path} ({kind})",
            "current": path == cur,
        })
    out.sort(key=lambda e: (not e["current"], e["label"].lower()))
    return out


# ------------------------------------------------------------ completion -----
def _environment():
    import jedi
    path = current_interpreter()
    if path not in _env_cache:
        # safe=False lets Jedi import the target env's site-packages for types.
        _env_cache[path] = jedi.create_environment(path, safe=False)
    return _env_cache[path]


def complete(code, line, column, limit=50):
    """Jedi completions at a 0-based (line, column). Returns a list of
    {name, insert, type, detail} sorted by Jedi's own relevance."""
    import jedi

    script = jedi.Script(code, environment=_environment())
    items = []
    for c in script.complete(line + 1, column):  # Jedi lines are 1-based
        items.append({
            "name": c.name,
            "insert": c.complete or "",   # text to append after the cursor
            "type": c.type,               # module/class/function/keyword/instance/...
            "detail": (c.description or "")[:80],
        })
        if len(items) >= limit:
            break
    return items
