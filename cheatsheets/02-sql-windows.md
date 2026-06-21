# SQL Window Functions

A window function computes across a set of rows **related to the current row**,
without collapsing them (unlike `GROUP BY`). Every row stays.

```sql
func() OVER (PARTITION BY ... ORDER BY ... <frame>)
```

- `PARTITION BY` - the groups (like GROUP BY, but rows survive).
- `ORDER BY` - ordering inside each partition (needed for ranking / running).
- frame - which rows in the partition the function sees (see below).

## Ranking: ROW_NUMBER vs RANK vs DENSE_RANK

On the ties `100, 90, 90, 80`:

| Function | Result | Behavior |
|----------|--------|----------|
| `ROW_NUMBER` | 1, 2, 3, 4 | always unique, arbitrary tie-break |
| `RANK` | 1, 2, 2, 4 | ties share, **then a gap** |
| `DENSE_RANK` | 1, 2, 2, 3 | ties share, **no gap** |

```sql
SELECT name, salary,
  ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) AS rn,
  RANK()       OVER (PARTITION BY dept ORDER BY salary DESC) AS rnk,
  DENSE_RANK() OVER (PARTITION BY dept ORDER BY salary DESC) AS dnk
FROM employees;
```

- **Top-N per group** → `ROW_NUMBER` (one row per rank slot).
- **Nth highest distinct value** → `DENSE_RANK` (ties count once).

## Why you can't filter a window in WHERE

Window functions run **after** `WHERE`/`GROUP BY`/`HAVING` (just before
`ORDER BY`). So `WHERE rn = 1` is invalid - `rn` doesn't exist yet. Wrap it:

```sql
SELECT * FROM (
  SELECT name, ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) rn
  FROM employees
) t WHERE rn <= 2;          -- or, in DuckDB/Postgres: ... QUALIFY rn <= 2
```

## Frames: the running-vs-grand-total trap

With an `ORDER BY` in the `OVER()`, the **default frame** becomes
`RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` - i.e. a **running** total.
With **no** `ORDER BY`, the frame is the whole partition - a **grand** total.

```sql
SELECT txn_id, amount,
  SUM(amount) OVER (PARTITION BY user_id ORDER BY txn_date) AS running,  -- cumulative
  SUM(amount) OVER (PARTITION BY user_id)                   AS grand     -- whole partition
FROM transactions;
```

Same `SUM(amount)`, two different numbers. Adding `ORDER BY` silently changed
the frame.

### ROWS vs RANGE

- `ROWS` - counts **physical rows** (`ROWS BETWEEN 2 PRECEDING AND CURRENT ROW`).
- `RANGE` - counts **value peers**; ties on the `ORDER BY` key are lumped
  together. With duplicate order keys, `RANGE` running totals jump at each tie
  group. Prefer `ROWS UNBOUNDED PRECEDING` for a precise per-row running total.

## LAG / LEAD - previous / next row

```sql
SELECT month, revenue,
  LAG(revenue)  OVER (ORDER BY month) AS prev_month,
  revenue - LAG(revenue) OVER (ORDER BY month) AS mom_change
FROM monthly;          -- first row: LAG is NULL -> change NULL
```

`LAG(col, n, default)` looks `n` rows back. `LEAD` looks forward - handy for
funnels ("did the next event happen?") and gap detection.
