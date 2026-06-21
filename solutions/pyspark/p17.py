# p17 salary bands via when().otherwise(), then groupBy + count.
from typing import Dict
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def solve(spark: SparkSession, dfs: Dict[str, DataFrame]) -> DataFrame:
    e = dfs["employees"]
    band = (F.when(F.col("salary") < 60000, "low")
            .when(F.col("salary") < 90000, "mid")
            .otherwise("high"))
    return (e.withColumn("band", band)
            .groupBy("band")
            .agg(F.count("*").alias("num_employees")))
