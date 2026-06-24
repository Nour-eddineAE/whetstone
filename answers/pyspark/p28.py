# p28 [sparkops/med]
# Implement solve(spark, events) -> DataFrame. Expected columns: user_id, view, signup, purchase, click, login
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def solve(spark: SparkSession, events: DataFrame) -> DataFrame:
    # TODO: replace with your solution
    raise NotImplementedError
