"""Per-problem grade status, persisted to disk so it survives a server restart.

Stored as a small JSON file at the project root (.status.json):
  {"p01:sql": "PASS" | "FAIL" | "SKIP", ...}
"""
import json

from pengine import config

STATUS_FILE = config.ROOT / ".status.json"


def _load():
    try:
        return json.loads(STATUS_FILE.read_text())
    except Exception:
        return {}


STATUS = _load()


def _save():
    try:
        STATUS_FILE.write_text(json.dumps(STATUS, indent=0))
    except Exception:
        pass


def key(pid, track):
    return f"{pid}:{track}"


def set_status(pid, track, status):
    STATUS[key(pid, track)] = status
    _save()


def get_status(pid, track):
    return STATUS.get(key(pid, track))
