"""Single source of truth for the project layout and shared constants.

Everything resolves off ROOT (the practice/ dir), so modules can live in
packages without caring where they sit on disk.
"""
from pathlib import Path

# pengine/ -> practice/
ROOT = Path(__file__).resolve().parent.parent

DATA = ROOT / "data"
DB = ROOT / "practice.duckdb"
PROBLEMS_DIR = ROOT / "problems"
ANSWERS_DIR = ROOT / "answers"
SOLUTIONS_DIR = ROOT / "solutions"
CHEATS_DIR = ROOT / "cheatsheets"

# answer/solution file extension per track
EXT = {"sql": "sql", "pyspark": "py"}
TRACKS = ("sql", "pyspark")

# seed tables, also the dfs keys exposed to PySpark answers
TABLES = ("employees", "departments", "events", "transactions", "user_tags")

# display order for the sidenav / scoreboard
CATEGORY_ORDER = ("joins", "window", "patterns", "sparkops")

# web server (override with env PRACTICE_HOST / PRACTICE_PORT)
import os
WEB_HOST = os.environ.get("PRACTICE_HOST", "127.0.0.1")
WEB_PORT = int(os.environ.get("PRACTICE_PORT", "9000"))
