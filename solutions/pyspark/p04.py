# p04 semi-join: employees with >=1 transaction, no row multiplication.
from typing import Dict
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def solve(spark: SparkSession, dfs: Dict[str, DataFrame]) -> DataFrame:
    e, t = dfs["employees"], dfs["transactions"]
    # left_semi keeps left rows that have a match, emits no right columns, no dups.
    return e.join(t, e.emp_id == t.user_id, "left_semi").select("emp_id", "name")
