# p25 multi-step: aggregate to dept totals, rank them, keep the top 3.
from typing import Dict
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def solve(spark: SparkSession, dfs: Dict[str, DataFrame]) -> DataFrame:
    totals = dfs["employees"].groupBy("dept").agg(F.sum("salary").alias("total_salary"))
    w = Window.orderBy(F.col("total_salary").desc())
    return (totals.withColumn("rnk", F.rank().over(w))
            .where(F.col("rnk") <= 3)
            .select("dept", "total_salary", "rnk"))
