# p19 distinct vs dropDuplicates, as three counts in one row.
from typing import Dict
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def solve(spark: SparkSession, dfs: Dict[str, DataFrame]) -> DataFrame:
    ev = dfs["events"]
    total = ev.count()
    distinct_all = ev.distinct().count()                       # whole-row dedup
    distinct_ue = ev.dropDuplicates(["user_id", "event_type"]).count()  # subset dedup
    return spark.createDataFrame(
        [(total, distinct_all, distinct_ue)],
        ["total", "distinct_all", "distinct_user_event"],
    )
