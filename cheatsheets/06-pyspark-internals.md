# PySpark Internals (the concepts that matter)

This is the conceptual core - whether you actually understand
Spark, not just the API.

## Transformations vs Actions (lazy evaluation)

- **Transformations** (`select`, `filter`, `join`, `groupBy`, `withColumn`) are
  **lazy** - they only build a logical plan (a DAG). Nothing runs yet.
- **Actions** (`collect`, `count`, `show`, `write`, `take`) **trigger
  execution**. Spark optimizes the whole DAG (Catalyst) and runs it.

```python
df2 = df.filter(...).select(...)   # nothing executes
df2.count()                        # NOW the job runs
```

Why it matters: Spark can fuse and reorder lazy steps (predicate pushdown,
column pruning) before running. Calling an action twice re-runs the lineage
unless you `cache()`.

## Narrow vs Wide transformations

- **Narrow** - each output partition depends on **one** input partition:
  `map`, `filter`, `select`, `withColumn`. No data movement. Cheap.
- **Wide** - output partitions depend on **many** input partitions, so data
  must move across the network: `groupBy`, `join`, `distinct`, `repartition`,
  `orderBy`. This movement is a **shuffle**.

## The Shuffle - the thing to minimize

A shuffle re-partitions data by a key across the cluster: write to disk →
transfer over network → read back. It's the dominant cost in most jobs.

Triggered by: `groupBy` / aggregations, `join` (non-broadcast), `distinct` /
`dropDuplicates`, `repartition`, `orderBy`, window functions with
`partitionBy`.

Reduce it: filter early (less data to shuffle), pre-aggregate, broadcast small
sides, pick a sensible `spark.sql.shuffle.partitions` (default 200 is often too
many for small data - this project sets 4).

## Broadcast join

When one side is small (~≤10s of MB), Spark can **broadcast** it to every
executor and join locally - **no shuffle** of the big table.

```python
from pyspark.sql.functions import broadcast
big.join(broadcast(small), "key")
```
Spark auto-broadcasts under `spark.sql.autoBroadcastJoinThreshold` (default
10MB). Force it with `broadcast()` when you know a side is small. Wrong-side or
too-large broadcasts cause OOM - that's the trade-off.

## repartition vs coalesce

| | Shuffle? | Use |
|--|----------|-----|
| `repartition(n)` | yes (full) | **increase** partitions, or rebalance skew |
| `repartition("key")` | yes | co-locate by key before a join/agg |
| `coalesce(n)` | no (merges) | **decrease** partitions cheaply (e.g. before write) |

`coalesce` only merges existing partitions (narrow), so it can't grow them and
can leave skew - but it avoids a shuffle.

## cache / persist

`df.cache()` (= `persist(MEMORY_AND_DISK)`) keeps a computed DataFrame in
memory so repeated actions don't recompute the lineage. Cache only when you
**reuse** a DataFrame multiple times; it costs memory and is itself lazy
(materializes on the next action). `unpersist()` when done.

## Skew

If one key has far more rows, its partition becomes a straggler (one slow task
holds up the stage). Mitigate with salting (add a random suffix to the key),
AQE skew-join handling (`spark.sql.adaptive.enabled`), or broadcasting.

## Why Spark over pandas?

pandas is single-machine, in-memory, eager. Spark is **distributed**, spills to
disk, and is **lazy** (optimizes the whole plan). Use pandas when it fits in RAM
on one box; reach for Spark when data exceeds memory / one machine, or you need
cluster parallelism. (For medium local data, DuckDB often beats both.)
