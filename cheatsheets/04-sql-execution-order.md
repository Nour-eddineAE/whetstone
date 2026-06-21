# SQL Logical Execution Order

SQL is written `SELECT ... FROM ...`, but it is **evaluated** in a different
order. Knowing it explains alias scope, where windows run, and WHERE vs HAVING.

```
1. FROM / JOIN      build and combine the source rows
2. WHERE            filter rows (no aggregates, no SELECT aliases yet)
3. GROUP BY         collapse into groups
4. HAVING           filter groups (aggregates allowed)
5. SELECT           compute expressions, window functions, assign aliases
6. DISTINCT         de-duplicate
7. ORDER BY         sort (can use SELECT aliases)
8. LIMIT / OFFSET   take the slice
```

## Consequences you get asked about

**Window functions run in step 5** (SELECT), after `WHERE`/`GROUP BY`/`HAVING`.
That's why you can't filter on `ROW_NUMBER()` in `WHERE` - it doesn't exist yet.
Wrap it in a subquery/CTE and filter outside (or use `QUALIFY`).

**SELECT aliases aren't visible in WHERE/GROUP BY/HAVING** (they're created in
step 5). They **are** visible in `ORDER BY` (step 7).

```sql
SELECT salary * 12 AS annual
FROM employees
WHERE annual > 100000      -- ERROR: 'annual' not defined yet
ORDER BY annual;           -- OK: ORDER BY runs after SELECT
```
Fix the WHERE by repeating the expression: `WHERE salary * 12 > 100000`.

**WHERE can't see aggregates** (step 2 is before grouping) → use `HAVING`.

**You can't reference a window function inside another's definition** in the
same SELECT - layer them with CTEs.

## Mental model

> Rows are **built** (FROM), **filtered** (WHERE), **grouped** (GROUP BY),
> **group-filtered** (HAVING), **projected** (SELECT, incl. windows),
> **deduped** (DISTINCT), **sorted** (ORDER BY), **sliced** (LIMIT).

If a step needs something a later step produces, you need another layer (a
subquery or CTE).
