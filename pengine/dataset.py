"""Read-only previews of the seed tables (sample rows for the problem view)."""
import datetime as dt
import decimal

import duckdb

from . import config


def _jsonable(v):
    if v is None or isinstance(v, (bool, int, str)):
        return v
    if isinstance(v, (float, decimal.Decimal)):
        return round(float(v), 4)
    if isinstance(v, (dt.date, dt.datetime)):
        return v.isoformat(sep=" ") if isinstance(v, dt.datetime) else v.isoformat()
    return str(v)


def sample(name, limit=5):
    """Return {columns, rows, total} for one seed table. Unknown table -> None."""
    if name not in config.TABLES:
        return None
    con = duckdb.connect(str(config.DB), read_only=True)
    try:
        cur = con.execute(f"SELECT * FROM {name} LIMIT {int(limit)}")
        cols = [d[0] for d in cur.description]
        rows = [[_jsonable(v) for v in r] for r in cur.fetchall()]
        total = con.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0]
    finally:
        con.close()
    return {"columns": cols, "rows": rows, "total": total}


def samples_for(tables, limit=5):
    """{table: sample(...)} for each valid table name."""
    return {t: sample(t, limit) for t in tables if t in config.TABLES}


def run_query(sql, limit=200):
    """Run an ad-hoc read-only query (the 'run selection' scratchpad). The
    read_only connection rejects any write/DDL, so this can't mutate the DB.
    Returns {columns, rows, truncated}. Raises on SQL error (caller handles)."""
    con = duckdb.connect(str(config.DB), read_only=True)
    try:
        cur = con.execute(sql)
        cols = [d[0] for d in cur.description] if cur.description else []
        raw = cur.fetchmany(limit + 1)
        truncated = len(raw) > limit
        rows = [[_jsonable(v) for v in r] for r in raw[:limit]]
        return {"columns": cols, "rows": rows, "truncated": truncated}
    finally:
        con.close()
