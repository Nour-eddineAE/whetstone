# p21 conditional aggregation: sum a 0/1 flag per band within each dept group.
from typing import Dict
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def solve(spark: SparkSession, dfs: Dict[str, DataFrame]) -> DataFrame:
    e = dfs["employees"]
    flag = lambda cond: F.sum(F.when(cond, 1).otherwise(0))
    return e.groupBy("dept").agg(
        flag(F.col("salary") < 60000).alias("low"),
        flag((F.col("salary") >= 60000) & (F.col("salary") < 90000)).alias("mid"),
        flag(F.col("salary") >= 90000).alias("high"),
    )
