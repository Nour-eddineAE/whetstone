# p15 [patterns/hard]
# Implement solve(spark, dfs) -> DataFrame. Expected columns: event_type, users
# dfs keys: employees, departments, events, transactions, user_tags
from typing import Dict
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def solve(spark: SparkSession, dfs: Dict[str, DataFrame]) -> DataFrame:
    # TODO: replace with your solution
    raise NotImplementedError
