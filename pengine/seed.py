"""Deterministic seed data -> practice.duckdb + data/*.parquet (+ csv), then
scaffold TODO answer stubs for any problem not started yet.

Reproducible: fixed random seed -> identical data every run.
"""
import datetime as dt
import random

import duckdb

from . import config, content, meta


def build_data():
    """Generate the tables and load them into DuckDB + parquet + csv."""
    random.seed(42)
    config.DATA.mkdir(exist_ok=True)

    # ------------------------------------------------------------ departments
    # dept_name is the join key into employees.dept. 'Operations' is intentionally
    # absent, so some employees stay unmatched (inner vs left join difference).
    departments = [(10, "Engineering"), (20, "Sales"), (30, "Marketing"),
                   (40, "HR"), (50, "Finance")]
    dept_names = [d[1] for d in departments]

    # -------------------------------------------------------------- employees
    # Salaries are multiples of 5000 so ties happen inside a dept -> RANK vs
    # DENSE_RANK differ. Top 6 are managers with NULL manager_id. ~5 sit in
    # 'Operations' (no department row).
    N = 60
    base_salary = {"Engineering": 110000, "Sales": 70000, "Marketing": 75000,
                   "HR": 60000, "Finance": 95000, "Operations": 65000}
    manager_pool = list(range(1, 7))
    employees = []
    for i in range(1, N + 1):
        if i <= 6:
            dept, mgr = dept_names[(i - 1) % len(dept_names)], None
        else:
            dept = "Operations" if i in (55, 56, 57, 58, 59) else random.choice(dept_names)
            mgr = random.choice(manager_pool)
        salary = max(40000, base_salary[dept] + random.randint(-3, 6) * 5000)
        hire = dt.date(2015, 1, 1) + dt.timedelta(days=random.randint(0, 3000))
        employees.append((i, f"Emp{i:02d}", dept, salary, mgr, hire))

    # ------------------------------------------------------------ transactions
    # user_id reuses emp_id space (1..30). Jan-Jun 2023 -> month-over-month works.
    transactions = []
    tid = 1000
    for _ in range(120):
        u = random.randint(1, 30)
        amt = round(random.uniform(5, 500), 2)
        d = dt.date(2023, random.randint(1, 6), random.randint(1, 28))
        transactions.append((tid, u, amt, d))
        tid += 1

    # ----------------------------------------------------------------- events
    # Funnel: every user views, ~70% signup, ~40% purchase. Plus clicks. Plus
    # login streaks (consecutive days) for gaps-and-islands. Plus exact dup rows.
    events = []
    users_e = list(range(1, 21))
    for u in users_e:
        base = dt.datetime(2023, 1, 1) + dt.timedelta(days=random.randint(0, 40))
        events.append((u, "view", base))
        if random.random() < 0.7:
            events.append((u, "signup", base + dt.timedelta(hours=1)))
        if random.random() < 0.4:
            events.append((u, "purchase", base + dt.timedelta(hours=2)))
        for _ in range(random.randint(0, 3)):
            events.append((u, "click", base + dt.timedelta(hours=random.randint(3, 20))))
    for u in users_e[:10]:
        start = dt.date(2023, 2, 1) + dt.timedelta(days=random.randint(0, 20))
        streak = random.randint(2, 6)
        for k in range(streak):
            events.append((u, "login", dt.datetime.combine(start + dt.timedelta(days=k), dt.time(9))))
        gap_start = start + dt.timedelta(days=streak + random.randint(2, 5))
        for k in range(random.randint(1, 3)):
            events.append((u, "login", dt.datetime.combine(gap_start + dt.timedelta(days=k), dt.time(9))))
    events.extend(random.sample(events, 8))  # intentional exact-duplicate rows

    # -------------------------------------------------------------- user_tags
    tag_pool = ["vip", "beta", "newsletter", "churn_risk", "enterprise"]
    user_tags = [(u, ",".join(random.sample(tag_pool, random.randint(1, 3))))
                 for u in range(1, 13)]

    # ----------------------------------------------------------- load duckdb
    schema = {
        "employees": ("emp_id INTEGER, name VARCHAR, dept VARCHAR, salary INTEGER, "
                      "manager_id INTEGER, hire_date DATE", employees),
        "departments": ("dept_id INTEGER, dept_name VARCHAR", departments),
        "events": ("user_id INTEGER, event_type VARCHAR, event_ts TIMESTAMP", events),
        "transactions": ("txn_id INTEGER, user_id INTEGER, amount DOUBLE, txn_date DATE", transactions),
        "user_tags": ("user_id INTEGER, tags VARCHAR", user_tags),
    }
    con = duckdb.connect(str(config.DB))
    for name, (cols, rows) in schema.items():
        con.execute(f"DROP TABLE IF EXISTS {name}")
        con.execute(f"CREATE TABLE {name} ({cols})")
        ph = ",".join("?" * len(rows[0]))
        con.executemany(f"INSERT INTO {name} VALUES ({ph})", rows)
        con.execute(f"COPY {name} TO '{config.DATA / (name + '.parquet')}' (FORMAT PARQUET)")
        con.execute(f"COPY {name} TO '{config.DATA / (name + '.csv')}' (HEADER, DELIMITER ',')")
        print(f"  {name:<13} {len(rows):>4} rows")
    con.close()


def scaffold_stubs():
    """Create TODO answer stubs for problems not started yet (never overwrite)."""
    made = 0
    for m in meta.all_meta():
        pid, cols, tag = m["id"], ", ".join(m["columns"]), f"{m['category']}/{m['difficulty']}"
        if "sql" in m["tracks"]:
            f = content.track_file(pid, "sql")
            if not f.exists():
                f.parent.mkdir(parents=True, exist_ok=True)
                f.write_text(f"-- {pid} [{tag}]\n-- TODO: write your SQL. Expected columns: {cols}\n"
                             f"-- (this TODO marker means 'not attempted' to the grader)\n"
                             f"SELECT 'TODO' AS todo;\n")
                made += 1
        if "pyspark" in m["tracks"]:
            f = content.track_file(pid, "pyspark")
            if not f.exists():
                f.parent.mkdir(parents=True, exist_ok=True)
                f.write_text(
                    f"# {pid} [{tag}]\n"
                    f"# Implement solve(spark, dfs) -> DataFrame. Expected columns: {cols}\n"
                    f"# dfs keys: {', '.join(config.TABLES)}\n"
                    f"from typing import Dict\n"
                    f"from pyspark.sql import DataFrame, SparkSession\n"
                    f"from pyspark.sql import functions as F\n"
                    f"from pyspark.sql.window import Window\n\n\n"
                    f"def solve(spark: SparkSession, dfs: Dict[str, DataFrame]) -> DataFrame:\n"
                    f"    # TODO: replace with your solution\n"
                    f"    raise NotImplementedError\n")
                made += 1
    return made


def main():
    build_data()
    made = scaffold_stubs()
    print(f"\nSeed complete -> {config.DB.name}")
    print(f"Scaffolded {made} new TODO stub(s) in answers/ (existing files left untouched).")


if __name__ == "__main__":
    main()
