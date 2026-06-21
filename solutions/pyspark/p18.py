# p18 explode: split the string into an array, explode to one row per tag.
from typing import Dict
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def solve(spark: SparkSession, dfs: Dict[str, DataFrame]) -> DataFrame:
    ut = dfs["user_tags"]
    return ut.select("user_id", F.explode(F.split("tags", ",")).alias("tag"))
