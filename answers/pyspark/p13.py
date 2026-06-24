# p13 [patterns/med]
# Implement solve(spark, events) -> DataFrame. Expected columns: user_id, event_type, event_ts
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def solve(spark: SparkSession, events: DataFrame) -> DataFrame:
    # TODO: replace with your solution
    raise NotImplementedError
