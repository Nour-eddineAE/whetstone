# SQL Joins

## The join types

| Join | Keeps | Use for |
|------|-------|---------|
| `INNER JOIN` | only rows matching on **both** sides | the common case |
| `LEFT JOIN` | every left row; right cols `NULL` when no match | "all X, with their Y if any" |
| `RIGHT JOIN` | every right row | rare; flip to LEFT instead |
| `FULL OUTER JOIN` | every row from both sides | reconciliation / diffs |
| `CROSS JOIN` | every combination (Cartesian) | calendars, grids |

```sql
SELECT e.emp_id, e.name, d.dept_id
FROM employees e
JOIN departments d ON e.dept = d.dept_name;   -- INNER: drops unmatched depts
```

## ON vs WHERE in an outer join (classic trap)

In a `LEFT JOIN`, a predicate on the **right** table belongs in `ON`, not
`WHERE`. Putting it in `WHERE` turns the outer join back into an inner join,
because `NULL` rows fail the filter.

```sql
-- keeps all employees, only attaching 2023 departments
LEFT JOIN departments d ON e.dept = d.dept_name AND d.created_year = 2023
-- BUG: silently drops employees with no dept (NULL fails the WHERE)
LEFT JOIN departments d ON e.dept = d.dept_name
WHERE d.created_year = 2023
```

Rule: filter the **left** table in `WHERE`, restrict the **right** table in `ON`.

## Semi-join - "rows that have a match" (no columns from the other table)

```sql
-- employees who made at least one transaction (each once, no fan-out)
SELECT e.* FROM employees e
WHERE EXISTS (SELECT 1 FROM transactions t WHERE t.user_id = e.emp_id);
```

`EXISTS` short-circuits on the first match and never duplicates rows - unlike
`JOIN`, which emits one row per match.

## Anti-join - "rows with NO match"

```sql
-- employees who are nobody's manager
SELECT e.* FROM employees e
WHERE NOT EXISTS (SELECT 1 FROM employees m WHERE m.manager_id = e.emp_id);
```

### The `NOT IN` null trap

```sql
-- returns ZERO rows if manager_id contains any NULL
WHERE emp_id NOT IN (SELECT manager_id FROM employees);
```

`x NOT IN (a, b, NULL)` is `x<>a AND x<>b AND x<>NULL`. The last term is
`UNKNOWN`, so the whole `AND` can never be `TRUE`. **Always** use `NOT EXISTS`
(or `LEFT JOIN ... WHERE right IS NULL`) for anti-joins on nullable columns.

## Fan-out (row multiplication)

Joining a one-to-many child multiplies the parent's rows. If you then `SUM`, you
**double-count**.

```sql
-- WRONG: each transaction is duplicated once per event of that user
SELECT e.dept, SUM(t.amount)
FROM employees e
JOIN transactions t ON t.user_id = e.emp_id
JOIN events ev      ON ev.user_id = e.emp_id   -- <-- fan-out
GROUP BY e.dept;
```

Fix: aggregate each child **separately** (pre-aggregate in subqueries / CTEs,
then join the aggregates), or just don't join what you don't need.

## Self-join

The same table twice under different aliases - for hierarchies and pairwise
comparisons.

```sql
-- employees earning more than their manager
SELECT e.name, e.salary, m.salary AS mgr_salary
FROM employees e JOIN employees m ON e.manager_id = m.emp_id
WHERE e.salary > m.salary;

-- unordered pairs in the same dept (no self, no mirror)
SELECT a.emp_id, b.emp_id
FROM employees a JOIN employees b
  ON a.dept = b.dept AND a.emp_id < b.emp_id;
```
