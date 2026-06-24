# p19 [sparkops/med]
# Implement solve(spark, events) -> DataFrame. Expected columns: total, distinct_all, distinct_user_event
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def solve(spark: SparkSession, events: DataFrame) -> DataFrame:
    # TODO: replace with your solution
    raise NotImplementedError
