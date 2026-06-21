"""JSON API routes. Thin wrappers over pengine - no business logic here."""
from flask import Blueprint, jsonify, request

from pengine import cheats, config, content, dataset, grader, meta

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
    m = meta.get(pid)
    return jsonify({
        "id": pid, "track": track, "category": m["category"],
        "difficulty": m["difficulty"], "ordered": m["ordered"],
        "columns": m["columns"], "tables": m["tables"], "tracks": m["tracks"],
        "prompt": m["prompt"], "hint": m.get("hint", ""),
        "answer": content.read_answer(pid, track),
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


@bp.get("/hint/<pid>")
def hint(pid):
    if pid not in meta.all_ids():
        return jsonify({"error": "unknown problem"}), 404
    return jsonify({"id": pid, "hint": content.get_hint(pid)})


@bp.get("/reveal/<pid>/<track>")
def reveal(pid, track):
    if not _valid(pid, track):
        return jsonify({"error": "unknown problem/track"}), 404
    return jsonify({"id": pid, "track": track,
                    "solution": content.read_solution(pid, track)})


@bp.get("/cheatsheets")
def cheatsheets():
    return jsonify({"sheets": cheats.list_sheets()})


@bp.get("/cheatsheet/<slug>")
def cheatsheet(slug):
    sheet = cheats.render(slug)
    if sheet is None:
        return jsonify({"error": "unknown cheat sheet"}), 404
    return jsonify(sheet)
