# p27 "above own-dept average". The idiomatic Spark form of a correlated
# subquery is a window aggregate over the partition (dept), then a filter.
from typing import Dict
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def solve(spark: SparkSession, dfs: Dict[str, DataFrame]) -> DataFrame:
    e = dfs["employees"]
    dept_avg = F.avg("salary").over(Window.partitionBy("dept"))
    return (e.withColumn("_dept_avg", dept_avg)
            .where(F.col("salary") > F.col("_dept_avg"))
            .select("emp_id", "name", "dept", "salary"))
