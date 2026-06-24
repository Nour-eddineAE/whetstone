"""Activity log: append-only event store powering the dashboard.

Events appended to .activity.ndjson (newline-delimited JSON) at the project root:
  {"ts": <unix>, "type": "problem_open",  "pid": "p01", "track": "sql"}
  {"ts": <unix>, "type": "problem_check", "pid": "p01", "track": "sql", "status": "PASS"}
  {"ts": <unix>, "type": "sheet_view",    "slug": "sql-joins", "subject": "SQL"}

Call record() from API route handlers; call dashboard_data() for GET /api/dashboard.
"""
import json
import time
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone

from pengine import cheats as _cheats
from pengine import config
from pengine import meta as _meta

LOG_FILE = config.ROOT / ".activity.ndjson"
_MAX_SESSION_SEC = 1800  # 30-minute cap per open→check delta


# ── write ─────────────────────────────────────────────────────────────────────

def record(event_type: str, **kwargs) -> None:
    entry = {"ts": int(time.time()), "type": event_type, **kwargs}
    try:
        with LOG_FILE.open("a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:
        pass


# ── read ──────────────────────────────────────────────────────────────────────

def _load() -> list[dict]:
    if not LOG_FILE.exists():
        return []
    events = []
    for line in LOG_FILE.read_text().splitlines():
        line = line.strip()
        if line:
            try:
                events.append(json.loads(line))
            except Exception:
                pass
    return events


# ── helpers ───────────────────────────────────────────────────────────────────

def _ts_to_date(ts: int) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")


def _streak(active_dates: set[str]) -> int:
    """Consecutive days with activity ending today (or yesterday if today has none)."""
    today = date.today()
    cursor = today if today.isoformat() in active_dates else today - timedelta(days=1)
    count = 0
    while cursor.isoformat() in active_dates:
        count += 1
        cursor -= timedelta(days=1)
    return count


def _week_minutes(events: list[dict]) -> int:
    """Approximate study time (minutes) in last 7 days via open→check deltas."""
    cutoff = int(time.time()) - 7 * 86400
    last_open: dict[tuple[str, str], int] = {}
    total_sec = 0
    for ev in events:
        t = ev.get("type")
        ts = ev.get("ts", 0)
        if t == "problem_open":
            last_open[(ev["pid"], ev["track"])] = ts
        elif t == "problem_check" and ts >= cutoff:
            open_ts = last_open.get((ev["pid"], ev["track"]))
            if open_ts is not None:
                total_sec += min(ts - open_ts, _MAX_SESSION_SEC)
    return total_sec // 60


# ── main computation ──────────────────────────────────────────────────────────

def dashboard_data(status: dict) -> dict:
    """Return structured dashboard payload derived from activity log + status."""
    events = _load()
    all_problems = _meta.all_meta()
    all_sheets = _cheats.list_sheets()

    # problems with PASS in any track
    solved_pids: set[str] = set()
    for pid_track, st in status.items():
        if st == "PASS":
            solved_pids.add(pid_track.split(":")[0])

    # ── category progress ─────────────────────────────────────────────────────
    cat_total: dict[str, int] = defaultdict(int)
    cat_solved: dict[str, int] = defaultdict(int)
    for pm in all_problems:
        cat = pm["category"]
        cat_total[cat] += 1
        if pm["id"] in solved_pids:
            cat_solved[cat] += 1

    ordered_cats = list(config.CATEGORY_ORDER)
    categories = []
    for cat in ordered_cats:
        if cat in cat_total:
            categories.append({
                "id": cat,
                "label": cat.title(),
                "solved": cat_solved.get(cat, 0),
                "total": cat_total[cat],
            })
    for cat in sorted(cat_total):
        if cat not in ordered_cats:
            categories.append({
                "id": cat,
                "label": cat.title(),
                "solved": cat_solved.get(cat, 0),
                "total": cat_total[cat],
            })

    # ── solved by difficulty ──────────────────────────────────────────────────
    diff_solved: dict[str, int] = defaultdict(int)
    for pm in all_problems:
        if pm["id"] in solved_pids:
            diff_solved[pm["difficulty"]] += 1

    # ── activity heatmap (last 180 days) ─────────────────────────────────────
    cutoff_180 = int(time.time()) - 180 * 86400
    day_count: dict[str, int] = defaultdict(int)
    active_dates: set[str] = set()
    for ev in events:
        ts = ev.get("ts", 0)
        if ts >= cutoff_180:
            d = _ts_to_date(ts)
            day_count[d] += 1
            active_dates.add(d)

    today = date.today()
    activity = [
        {"date": (today - timedelta(days=i)).isoformat(),
         "count": day_count.get((today - timedelta(days=i)).isoformat(), 0)}
        for i in range(179, -1, -1)
    ]

    # ── recent sheets (last 3 unique) ─────────────────────────────────────────
    slug_meta = {s["slug"]: s for s in all_sheets}
    seen: set[str] = set()
    recent: list[dict] = []
    for ev in reversed(events):
        if ev.get("type") == "sheet_view":
            slug = ev.get("slug", "")
            if slug and slug not in seen and slug in slug_meta:
                seen.add(slug)
                sm = slug_meta[slug]
                recent.append({
                    "slug": slug, "title": sm["title"],
                    "subject": sm["subject"], "ts": ev["ts"],
                })
        if len(recent) >= 3:
            break

    # ── score ─────────────────────────────────────────────────────────────────
    pass_count = sum(1 for v in status.values() if v == "PASS")
    attempted = sum(1 for v in status.values() if v in ("PASS", "FAIL"))
    score = round(100 * pass_count / attempted) if attempted else 0

    # ── sheets reviewed ───────────────────────────────────────────────────────
    viewed_slugs = {ev["slug"] for ev in events
                    if ev.get("type") == "sheet_view" and ev.get("slug")}

    return {
        "kpis": {
            "sheetsReviewed": {"count": len(viewed_slugs), "total": len(all_sheets)},
            "solved": {
                "easy": diff_solved.get("easy", 0),
                "med": diff_solved.get("med", 0),
                "hard": diff_solved.get("hard", 0),
                "total": len(solved_pids),
                "possible": len(all_problems),
            },
            "streak": _streak(active_dates),
            "score": score,
            "weekMinutes": _week_minutes(events),
        },
        "categories": categories,
        "activity": activity,
        "recent": recent,
    }
