# SQL Aggregation

## COUNT variants (they differ on NULLs and duplicates)

| Expression | Counts |
|------------|--------|
| `COUNT(*)` | all rows (NULLs included) |
| `COUNT(col)` | rows where `col IS NOT NULL` |
| `COUNT(DISTINCT col)` | distinct non-NULL values of `col` |

```sql
SELECT COUNT(*)              AS rows,        -- 100
       COUNT(manager_id)     AS has_mgr,     -- 94 (6 NULLs skipped)
       COUNT(DISTINCT dept)  AS n_depts      -- 5
FROM employees;
```

## NULLs are skipped by aggregates - the AVG denominator trap

`SUM`, `AVG`, `MIN`, `MAX` **ignore NULLs**. So `AVG(col)` divides by the count
of **non-NULL** values, not by row count.

```sql
-- values: 10, 20, NULL
AVG(x)                     -- = 15  (30 / 2)
SUM(x) / COUNT(*)          -- = 10  (30 / 3)   <- different!
```

If NULL should mean zero, coalesce first: `AVG(COALESCE(x, 0))`.

## The GROUP BY rule

Every column in `SELECT` must be either inside an aggregate **or** in the
`GROUP BY`. Otherwise the value is ambiguous (which row's `name`?).

```sql
SELECT dept, COUNT(*), AVG(salary)
FROM employees
GROUP BY dept;            -- dept is grouped; the rest are aggregated
```

## WHERE vs HAVING

- `WHERE` filters **rows before** grouping (can't see aggregates).
- `HAVING` filters **groups after** aggregation (can use aggregates).

```sql
SELECT dept, AVG(salary) AS avg_sal, COUNT(*) AS headcount
FROM employees
WHERE hire_date >= DATE '2018-01-01'   -- per-row filter
GROUP BY dept
HAVING COUNT(*) > 5 AND AVG(salary) > 70000;   -- per-group filter
```

## Conditional aggregation - pivot without PIVOT

`SUM(CASE WHEN cond THEN 1 ELSE 0 END)` (or `COUNT(CASE WHEN cond THEN 1 END)`)
turns rows into columns. The single most useful aggregation trick.

```sql
SELECT dept,
  SUM(CASE WHEN salary <  60000 THEN 1 ELSE 0 END) AS low,
  SUM(CASE WHEN salary >= 90000 THEN 1 ELSE 0 END) AS high,
  AVG(CASE WHEN salary >= 90000 THEN salary END)   AS avg_high_salary
FROM employees
GROUP BY dept;
```

`FILTER` is the cleaner ANSI form (DuckDB/Postgres):
`COUNT(*) FILTER (WHERE salary < 60000)`.

## Gotchas

- `SUM` of no rows is `NULL`, not `0` - wrap in `COALESCE(SUM(x), 0)`.
- `COUNT(*)` of an empty group is `0` (a group only exists if it has a row).
- Aggregates can't nest: `SUM(AVG(x))` is illegal - use a subquery / CTE.
