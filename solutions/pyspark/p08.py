# p08 top-2 per dept: row_number in a window, then filter rn <= 2.
from typing import Dict
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def solve(spark: SparkSession, dfs: Dict[str, DataFrame]) -> DataFrame:
    e = dfs["employees"]
    w = Window.partitionBy("dept").orderBy(F.col("salary").desc(), F.col("emp_id"))
    return (e.withColumn("rn", F.row_number().over(w))
            .where(F.col("rn") <= 2)
            .select("dept", "emp_id", "name", "salary", "rn"))
