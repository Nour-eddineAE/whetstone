# p26 [dates/med]
# Implement solve(spark, transactions) -> DataFrame. Expected columns: month, txn_count, total_amount
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def solve(spark: SparkSession, transactions: DataFrame) -> DataFrame:
    # TODO: replace with your solution
    raise NotImplementedError
