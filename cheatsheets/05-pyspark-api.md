# PySpark DataFrame API

## SQL → PySpark translation

| SQL | PySpark |
|-----|---------|
| `SELECT a, b` | `df.select("a", "b")` |
| `WHERE x > 1` | `df.filter(F.col("x") > 1)` / `df.where(...)` |
| `SELECT x AS y` | `df.withColumnRenamed("x","y")` or `F.col("x").alias("y")` |
| computed col | `df.withColumn("y", F.col("x") * 2)` |
| `GROUP BY d` agg | `df.groupBy("d").agg(F.sum("x").alias("s"))` |
| `ORDER BY x DESC` | `df.orderBy(F.col("x").desc())` |
| `JOIN ... ON` | `a.join(b, a.k == b.k, "inner")` |
| `UNION ALL` | `a.unionByName(b)` |
| `COUNT(DISTINCT x)` | `F.countDistinct("x")` |
| `LIMIT 10` | `df.limit(10)` |
| window | `F.row_number().over(Window.partitionBy(...).orderBy(...))` |

```python
from pyspark.sql import functions as F
from pyspark.sql.window import Window
```

## Columns: string vs Column

Most ops accept a column **name string** or a `Column` object. You need a real
`Column` (`F.col("x")`) to do arithmetic, comparisons, or call methods.

```python
df.select("salary")                       # string OK
df.select((F.col("salary") * 12).alias("annual"))   # need F.col for math
```

## Conditionals: when / otherwise

```python
band = (F.when(F.col("salary") < 60000, "low")
         .when(F.col("salary") < 90000, "mid")
         .otherwise("high"))
df.withColumn("band", band)
```

## NULL handling

```python
df.na.fill(0)                       # fill all numeric NULLs with 0
df.na.fill({"manager_id": -1})      # per-column
df.na.drop(subset=["dept"])         # drop rows where dept is NULL
F.coalesce(F.col("a"), F.lit(0))    # first non-null
```

## distinct vs dropDuplicates

```python
df.distinct()                       # dedupe on ALL columns
df.dropDuplicates(["user_id", "event_type"])   # dedupe on a SUBSET
```

`dropDuplicates(subset)` keeps an arbitrary row per key - pair it with a window
`row_number()` if you need a *specific* one (e.g. latest).

## explode - array → rows

```python
df.select("user_id", F.explode(F.split("tags", ",")).alias("tag"))
```
`explode` drops empty arrays; `explode_outer` keeps them (emits NULL).

## Aggregations

```python
df.groupBy("dept").agg(
    F.count("*").alias("n"),
    F.countDistinct("user_id").alias("users"),
    F.sum("amount").alias("total"),
    F.expr("percentile(amount, 0.5)").alias("median"),
)
```

## pivot

```python
(df.groupBy("user_id")
   .pivot("event_type", ["view", "signup", "purchase"])  # value list = fixed cols + speed
   .count()
   .na.fill(0))
```
Always pass the value list - without it Spark scans the data first (an extra
job) and column order/presence becomes data-dependent.
