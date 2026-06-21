"""The grader - pure logic, no I/O presentation.

`grade_result(track, pid, ref=False)` is the SINGLE SOURCE OF TRUTH for grading.
Both the CLI (check.py) and the web app call it; neither reimplements comparison.

Comparison rules: values only, column NAMES ignored, column ORDER matters,
floats to 4dp, dates/timestamps by ISO value, order-insensitive unless the
problem sets `ordered: true`.
"""
import datetime as dt
import decimal
import importlib.util

import duckdb

from . import config, content, meta


# ----------------------------------------------------------------- normalize
def _nv(v):
    if v is None:
        return None
    if isinstance(v, bool):
        return v
    if isinstance(v, (float, decimal.Decimal)):
        return round(float(v), 4)
    if isinstance(v, dt.datetime):
        return v.isoformat(sep=" ")
    if isinstance(v, dt.date):
        return v.isoformat()
    return v


def _norm(rows):
    # tuples -> JSON-safe lists of normalized scalars
    return [[_nv(x) for x in r] for r in rows]


def compare(expected, actual, ordered):
    e, a = _norm(expected), _norm(actual)
    if ordered:
        return e == a
    return sorted(e, key=repr) == sorted(a, key=repr)


def diff(expected, actual, ordered):
    """Structured, JSON-safe diff over raw rows."""
    e, a = _norm(expected), _norm(actual)
    out = {"only_expected": [], "only_actual": [], "first_diff": None,
           "col_count_mismatch": None}
    if e and a and len(e[0]) != len(a[0]):
        out["col_count_mismatch"] = [len(e[0]), len(a[0])]
    if ordered:
        for i, (er, ar) in enumerate(zip(e, a)):
            if er != ar:
                out["first_diff"] = {"index": i, "expected": er, "actual": ar}
                break
        if out["first_diff"] is None and len(e) != len(a):
            out["first_diff"] = {"index": min(len(e), len(a)),
                                 "expected": e[len(a):len(a) + 1] or None,
                                 "actual": a[len(e):len(e) + 1] or None}
        return out
    es, as_ = set(map(repr, e)), set(map(repr, a))
    out["only_expected"] = [r for r in e if repr(r) not in as_][:10]
    out["only_actual"] = [r for r in a if repr(r) not in es][:10]
    return out


# ---------------------------------------------------------------------- SQL
class NotAttempted(Exception):
    pass


def _sql_text(pid, ref):
    f = content.track_file(pid, "sql", ref)
    if not f.exists():
        raise NotAttempted("no SQL file")
    txt = f.read_text()
    if not ref and "-- TODO" in txt:
        raise NotAttempted("TODO stub")
    return txt


def run_sql(text):
    con = duckdb.connect(str(config.DB), read_only=True)
    try:
        return con.execute(text).fetchall()
    finally:
        con.close()


# ------------------------------------------------------------------- PySpark
_spark = None
_dfs = None


def spark_ctx():
    """One warm SparkSession + cached DataFrames, reused for every check."""
    global _spark, _dfs
    if _spark is None:
        from pyspark.sql import SparkSession
        _spark = (SparkSession.builder.master("local[*]").appName("grader")
                  .config("spark.sql.shuffle.partitions", "4")
                  .config("spark.ui.enabled", "false")
                  .config("spark.sql.session.timeZone", "UTC")
                  .getOrCreate())
        _spark.sparkContext.setLogLevel("ERROR")
        _dfs = {n: _spark.read.parquet(str(config.DATA / f"{n}.parquet"))
                for n in config.TABLES}
    return _spark, _dfs


def _load_solve(pid, ref):
    f = content.track_file(pid, "pyspark", ref)
    if not f.exists():
        raise NotAttempted("no PySpark file")
    # Fresh import EVERY call: the long-running server must never serve a stale
    # solve() after the answer file is edited. A fresh spec + module object
    # (never inserted into sys.modules) re-reads the file each time.
    importlib.invalidate_caches()
    spec = importlib.util.spec_from_file_location(
        f"_grade_{'ref' if ref else 'ans'}_{pid}", f)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if not hasattr(mod, "solve"):
        raise NotAttempted("no solve()")
    return mod.solve


def run_pyspark(pid, ref):
    spark, dfs = spark_ctx()
    solve = _load_solve(pid, ref)
    try:
        df = solve(spark, dfs)
    except NotImplementedError:
        raise NotAttempted("solve() not implemented")
    if df is None:
        raise NotAttempted("solve() returned None")
    return [tuple(r) for r in df.collect()]


# --------------------------------------------------------------------- grade
def grade_result(track, pid, ref=False):
    """Grade one (track, problem). Returns a JSON-safe dict:
      status PASS|FAIL|SKIP, passed, error, ordered, columns, category,
      difficulty, expected_count, actual_count,
      diff{only_expected, only_actual, first_diff, col_count_mismatch}.
    """
    m = meta.get(pid)
    base = {"pid": pid, "track": track, "ordered": m["ordered"],
            "columns": m["columns"], "category": m["category"],
            "difficulty": m["difficulty"], "passed": False, "error": None,
            "expected_count": 0, "actual_count": 0,
            "diff": {"only_expected": [], "only_actual": [], "first_diff": None,
                     "col_count_mismatch": None}}
    if track not in m["tracks"]:
        return {**base, "status": "SKIP", "error": "track not available"}
    try:
        if track == "sql":
            actual = run_sql(_sql_text(pid, ref))
            expected = run_sql(_sql_text(pid, True))
        else:
            actual = run_pyspark(pid, ref)
            expected = run_pyspark(pid, True)
    except NotAttempted as e:
        return {**base, "status": "SKIP", "error": str(e)}
    except Exception as e:
        return {**base, "status": "FAIL", "error": f"{type(e).__name__}: {e}"}

    ok = compare(expected, actual, m["ordered"])
    return {**base, "status": "PASS" if ok else "FAIL", "passed": ok,
            "expected_count": len(expected), "actual_count": len(actual),
            "diff": diff(expected, actual, m["ordered"])}
