# Rapid-Fire Conceptual Q&A

Short, spoken-answer questions. Aim for 1-2 crisp sentences each.

## SQL

**Q: WHERE vs HAVING?**
WHERE filters rows before grouping; HAVING filters groups after aggregation and
can reference aggregates.

**Q: Why does `NOT IN` with a NULL return nothing?**
`x NOT IN (..., NULL)` includes `x <> NULL`, which is UNKNOWN, so the AND is
never TRUE. Use `NOT EXISTS`.

**Q: RANK vs DENSE_RANK vs ROW_NUMBER?**
ROW_NUMBER is always unique; RANK shares ties then gaps; DENSE_RANK shares ties
with no gap.

**Q: Why can't you put a window function in WHERE?**
Windows are computed in SELECT, after WHERE. Wrap in a subquery/CTE (or QUALIFY).

**Q: INNER vs LEFT JOIN, and the outer-join filter trap?**
INNER keeps matches only; LEFT keeps all left rows. Filtering the right table in
WHERE turns a LEFT JOIN back into INNER - restrict the right table in ON.

**Q: COUNT(*) vs COUNT(col)?**
`COUNT(*)` counts rows; `COUNT(col)` skips NULLs in that column.

**Q: What is fan-out?**
Joining a one-to-many child multiplies parent rows, so a later SUM double-counts.
Aggregate children separately.

**Q: SQL logical execution order?**
FROM → WHERE → GROUP BY → HAVING → SELECT (windows here) → DISTINCT → ORDER BY →
LIMIT.

**Q: CTE vs subquery?**
Same power; CTEs read top-down and can be referenced multiple times / recurse.
Mostly readability.

## PySpark / Spark

**Q: Transformation vs action?**
Transformations are lazy (build the DAG); actions (collect/count/write) trigger
execution.

**Q: What is a shuffle and what causes it?**
Moving data across the network to re-partition by key. Caused by groupBy, join,
distinct, repartition, orderBy. It's the main cost.

**Q: Narrow vs wide transformation?**
Narrow: one input partition → one output (map/filter), no shuffle. Wide: many →
many (groupBy/join), requires a shuffle.

**Q: When and why a broadcast join?**
When one side is small: ship it to every executor and join locally, avoiding a
shuffle of the big table. Too large → OOM.

**Q: repartition vs coalesce?**
repartition does a full shuffle (can increase partitions / rebalance); coalesce
merges partitions without a shuffle (only decreases).

**Q: When to cache?**
When you reuse a DataFrame across multiple actions - it avoids recomputing the
lineage. Costs memory; unpersist when done.

**Q: What is data skew and how to fix it?**
One key has disproportionate rows → a straggler task. Fix with salting,
broadcast, or AQE skew handling.

**Q: distinct vs dropDuplicates?**
distinct dedupes on all columns; dropDuplicates(subset) on chosen columns
(keeping an arbitrary row per key).

**Q: Why Spark over pandas?**
Distributed, lazy/optimized, spills to disk - for data bigger than one machine's
memory. pandas (or DuckDB) is better when it fits on one box.

**Q: How does Catalyst help?**
It optimizes the logical plan before execution: predicate pushdown, column
pruning, join reordering - enabled by laziness.
