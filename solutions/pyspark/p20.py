# p20 null handling: coalesce NULL manager_id to -1.
from typing import Dict
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def solve(spark: SparkSession, dfs: Dict[str, DataFrame]) -> DataFrame:
    e = dfs["employees"]
    return e.select(
        "emp_id",
        F.coalesce(F.col("manager_id"), F.lit(-1)).alias("manager_id_filled"),
    )
