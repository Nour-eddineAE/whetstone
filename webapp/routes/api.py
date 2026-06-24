"""JSON API routes. Thin wrappers over pengine - no business logic here."""
from flask import Blueprint, jsonify, request

from pengine import cheats, config, content, dataset, grader, meta, pyenv

from ..activity import dashboard_data, record
from ..state import STATUS, get_status, set_status

bp = Blueprint("api", __name__, url_prefix="/api")


def _valid(pid, track):
    return track in config.EXT and pid in meta.all_ids()


@bp.get("/problems")
def problems():
    items = [{
        "id": m["id"], "category": m["category"], "difficulty": m["difficulty"],
        "ordered": m["ordered"], "tracks": m["tracks"],
        "columns": m["columns"], "tables": m["tables"],
    } for m in meta.all_meta()]
    return jsonify({"problems": items, "status": STATUS})


@bp.get("/problem/<pid>/<track>")
def problem(pid, track):
    if not _valid(pid, track):
        return jsonify({"error": "unknown problem/track"}), 404
    record("problem_open", pid=pid, track=track)
    m = meta.get(pid)
    return jsonify({
        "id": pid, "track": track, "category": m["category"],
        "difficulty": m["difficulty"], "ordered": m["ordered"],
        "columns": m["columns"], "tables": m["tables"], "tracks": m["tracks"],
        "prompt": m["prompt"], "hint": content.get_hint(pid, track),
        "answer": (content.strip_pyspark_imports(content.read_answer(pid, track))
                   if track == "pyspark" else content.read_answer(pid, track)),
        "status": get_status(pid, track),
        "samples": dataset.samples_for(m["tables"]),
    })


@bp.post("/answer/<pid>/<track>")
def save(pid, track):
    if not _valid(pid, track):
        return jsonify({"error": "unknown problem/track"}), 404
    text = (request.get_json(silent=True) or {}).get("text", "")
    content.write_answer(pid, track, text)
    return jsonify({"saved": True})


@bp.post("/check/<pid>/<track>")
def check(pid, track):
    if not _valid(pid, track):
        return jsonify({"error": "unknown problem/track"}), 404
    # Save editor bytes first (when sent), then grade THAT file -> UI and CLI
    # never diverge. With no "text" (scoreboard re-run) grade the file as-is.
    payload = request.get_json(silent=True) or {}
    if "text" in payload:
        content.write_answer(pid, track, payload["text"])
    res = grader.grade_result(track, pid)   # fresh import inside -> no stale solve()
    set_status(pid, track, res["status"])
    record("problem_check", pid=pid, track=track, status=res["status"])
    return jsonify(res)


@bp.post("/run/sql")
def run_sql_scratch():
    """Run ad-hoc SQL read-only (the 'run selection' scratchpad). Not graded,
    not saved. read_only connection blocks any write."""
    sql = (request.get_json(silent=True) or {}).get("sql", "").strip()
    if not sql:
        return jsonify({"error": "empty query"}), 400
    try:
        return jsonify(dataset.run_query(sql))
    except Exception as e:
        return jsonify({"error": f"{type(e).__name__}: {e}"})


@bp.get("/hint/<pid>/<track>")
def hint(pid, track):
    if pid not in meta.all_ids():
        return jsonify({"error": "unknown problem"}), 404
    return jsonify({"id": pid, "track": track, "hint": content.get_hint(pid, track)})


@bp.get("/reveal/<pid>/<track>")
def reveal(pid, track):
    if not _valid(pid, track):
        return jsonify({"error": "unknown problem/track"}), 404
    return jsonify({"id": pid, "track": track,
                    "solution": content.read_solution(pid, track)})


@bp.get("/environments")
def environments():
    """Discovered Python interpreters + the one currently selected."""
    return jsonify({"environments": pyenv.discover_environments(),
                    "current": pyenv.current_interpreter()})


@bp.post("/settings/interpreter")
def set_interpreter():
    path = (request.get_json(silent=True) or {}).get("path", "")
    try:
        return jsonify({"interpreter": pyenv.set_interpreter(path)})
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 400


@bp.post("/complete/python")
def complete_python():
    """Env-aware Python completions via Jedi. Never 500s on a bad parse -- the
    editor just shows nothing if completion fails."""
    p = request.get_json(silent=True) or {}
    try:
        items = pyenv.complete(p.get("code", ""), int(p.get("line", 0)), int(p.get("ch", 0)))
        return jsonify({"completions": items})
    except Exception as e:
        return jsonify({"completions": [], "error": f"{type(e).__name__}: {e}"})


@bp.post("/signature/python")
def signature_python():
    """Call signatures at the cursor (non-empty only when inside a call's parens).
    Powers context-aware param hints. Never 500s."""
    p = request.get_json(silent=True) or {}
    try:
        sigs = pyenv.signatures(p.get("code", ""), int(p.get("line", 0)), int(p.get("ch", 0)))
        return jsonify({"signatures": sigs})
    except Exception as e:
        return jsonify({"signatures": [], "error": f"{type(e).__name__}: {e}"})


@bp.post("/hover/python")
def hover_python():
    """Signature + docstring for the name under the cursor, for hover tooltips."""
    p = request.get_json(silent=True) or {}
    try:
        info = pyenv.hover(p.get("code", ""), int(p.get("line", 0)), int(p.get("ch", 0)))
        return jsonify({"info": info})
    except Exception as e:
        return jsonify({"info": None, "error": f"{type(e).__name__}: {e}"})


@bp.get("/dashboard")
def dashboard():
    return jsonify(dashboard_data(STATUS))


@bp.get("/cheatsheets")
def cheatsheets():
    return jsonify({"sheets": cheats.list_sheets()})


@bp.get("/cheatsheet/<slug>")
def cheatsheet(slug):
    sheet = cheats.render(slug)
    if sheet is None:
        return jsonify({"error": "unknown cheat sheet"}), 404
    record("sheet_view", slug=slug)
    return jsonify(sheet)
