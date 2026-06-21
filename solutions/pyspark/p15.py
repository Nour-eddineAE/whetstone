# p15 funnel. countDistinct per step, then explicit funnel ordering (order matters).
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def solve(spark, dfs):
    ev = dfs["events"].where(F.col("event_type").isin("view", "signup", "purchase"))
    counts = ev.groupBy("event_type").agg(F.countDistinct("user_id").alias("users"))
    order = (F.when(F.col("event_type") == "view", 1)
             .when(F.col("event_type") == "signup", 2)
             .otherwise(3))
    return counts.orderBy(order).select("event_type", "users")
