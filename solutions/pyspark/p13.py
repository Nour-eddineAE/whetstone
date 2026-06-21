# p13 dedup keep-latest: max(event_ts) per (user_id, event_type).
from typing import Dict
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def solve(spark: SparkSession, dfs: Dict[str, DataFrame]) -> DataFrame:
    ev = dfs["events"]
    return (ev.groupBy("user_id", "event_type")
            .agg(F.max("event_ts").alias("event_ts")))
