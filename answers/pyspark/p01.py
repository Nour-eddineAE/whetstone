# p01 [joins/easy]
# Implement solve(spark, dfs) -> DataFrame. Expected columns: emp_id, name, dept_id
# dfs keys: employees, departments, events, transactions, user_tags
from typing import Dict
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col
from pyspark.sql.window import Window


def solve(spark: SparkSession, dfs: Dict[str, DataFrame]) -> DataFrame:
    # TODO: replace with your solution
    return dfs["employees"].join(dfs["departments"], dfs["employees"]["dept"] == dfs["departments"]["dept_name"]).select("emp_id", "name", "dept_id") 