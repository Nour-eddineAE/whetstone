# Canonical Patterns

Recognize the shape → reach for the tool. These cover ~80% of real SQL/Spark work.

| Ask | Pattern |
|-----|---------|
| Nth highest / top-N per group | `ROW_NUMBER`/`DENSE_RANK` in subquery, filter outside |
| Latest row per key (dedup) | `ROW_NUMBER` ordered by ts DESC, keep `= 1` |
| Consecutive runs / streaks | gaps-and-islands: `date - ROW_NUMBER()` |
| Step-to-step conversion | funnel: `COUNT(DISTINCT)` per step / `LEAD` |
| Middle value | median: `percentile` / `percentile_approx` |
| Cumulative / period totals | window `SUM` with frame, `LAG` for deltas |
| Rows → columns | conditional aggregation `SUM(CASE WHEN)` / pivot |

## Nth highest (distinct)

```sql
SELECT DISTINCT salary FROM (
  SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) r FROM employees
) t WHERE r = :n;          -- DENSE_RANK so ties count once
```

## Dedup, keep latest

```sql
SELECT * FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY user_id, event_type
                               ORDER BY event_ts DESC) rn
  FROM events
) t WHERE rn = 1;
```
`MAX(event_ts)` works if you only need the timestamp; `ROW_NUMBER` when you need
the **whole latest row**.

## Gaps and islands (consecutive days)

For a sorted date series, `date - ROW_NUMBER()` is **constant** within a
consecutive run (both increase by 1/day). Group by that constant = the island.

```sql
WITH d AS (SELECT DISTINCT user_id, CAST(event_ts AS DATE) dt
           FROM events WHERE event_type='login'),
g AS (SELECT user_id, dt,
        dt - CAST(ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY dt) AS INT) AS grp
      FROM d)
SELECT user_id, MAX(cnt) FROM (
  SELECT user_id, grp, COUNT(*) cnt FROM g GROUP BY user_id, grp
) GROUP BY user_id;
```

## Funnel (distinct users per step)

```sql
SELECT event_type, COUNT(DISTINCT user_id) users
FROM events WHERE event_type IN ('view','signup','purchase')
GROUP BY event_type
ORDER BY CASE event_type WHEN 'view' THEN 1 WHEN 'signup' THEN 2 ELSE 3 END;
```
Strict ordering ("signup *after* view")? Self-join on user with `LEAD`/timestamp
comparison, or `MAX(CASE WHEN step='view' THEN ts END)` per user.

## Median

```sql
SELECT user_id, median(amount) FROM transactions GROUP BY user_id;  -- DuckDB
```
```python
df.groupBy("user_id").agg(F.expr("percentile(amount, 0.5)").alias("median"))  # exact
# F.percentile_approx("amount", 0.5) on big data (faster, approximate)
```

## Running total

```sql
SUM(amount) OVER (PARTITION BY user_id ORDER BY txn_date
                  ROWS UNBOUNDED PRECEDING)
```
