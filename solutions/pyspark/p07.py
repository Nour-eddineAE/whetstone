# p07 RANK vs DENSE_RANK over the same window. rank() leaves gaps, dense_rank() doesn't.
from typing import Dict
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def solve(spark: SparkSession, dfs: Dict[str, DataFrame]) -> DataFrame:
    e = dfs["employees"]
    w = Window.partitionBy("dept").orderBy(F.col("salary").desc())
    return e.select(
        "emp_id", "dept", "salary",
        F.rank().over(w).alias("rnk"),
        F.dense_rank().over(w).alias("dense_rnk"),
    )
