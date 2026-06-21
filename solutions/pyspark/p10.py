# p10 month-over-month. Aggregate monthly first, then lag() over month order.
from typing import Dict
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def solve(spark: SparkSession, dfs: Dict[str, DataFrame]) -> DataFrame:
    t = dfs["transactions"]
    monthly = (t.withColumn("month", F.date_format("txn_date", "yyyy-MM"))
               .groupBy("month")
               .agg(F.sum("amount").alias("monthly_amount")))
    w = Window.orderBy("month")
    return monthly.select(
        "month", "monthly_amount",
        F.lag("monthly_amount").over(w).alias("prev_amount"),
        (F.col("monthly_amount") - F.lag("monthly_amount").over(w)).alias("mom_change"),
    )
