# p10 [window/hard]
# Implement solve(spark, transactions) -> DataFrame. Expected columns: month, monthly_amount, prev_amount, mom_change
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def solve(spark: SparkSession, transactions: DataFrame) -> DataFrame:
    # TODO: replace with your solution
    raise NotImplementedError
