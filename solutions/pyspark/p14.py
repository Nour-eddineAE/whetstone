# p14 gaps-and-islands. date_sub(dt, row_number) is constant within a run of
# consecutive days; group by it, count, take the max per user.
from typing import Dict
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def solve(spark: SparkSession, dfs: Dict[str, DataFrame]) -> DataFrame:
    days = (dfs["events"].where(F.col("event_type") == "login")
            .select("user_id", F.to_date("event_ts").alias("dt"))
            .distinct())
    w = Window.partitionBy("user_id").orderBy("dt")
    grouped = (days.withColumn("rn", F.row_number().over(w))
               .withColumn("grp", F.expr("date_sub(dt, rn)")))
    streaks = grouped.groupBy("user_id", "grp").agg(F.count("*").alias("streak"))
    return streaks.groupBy("user_id").agg(F.max("streak").alias("max_streak"))
