# p09 [window/med]
# Implement solve(spark, transactions) -> DataFrame. Expected columns: user_id, txn_id, txn_date, amount, running_total
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def solve(spark: SparkSession, transactions: DataFrame) -> DataFrame:
    # TODO: replace with your solution
    raise NotImplementedError
