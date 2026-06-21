# p11 frame trap. Same F.sum('amount'): with an ordered row-frame it is a running
# total; with only partitionBy (no order, full frame) it is the grand total.
from typing import Dict
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def solve(spark: SparkSession, dfs: Dict[str, DataFrame]) -> DataFrame:
    t = dfs["transactions"]
    w_run = (Window.partitionBy("user_id").orderBy("txn_date", "txn_id")
             .rowsBetween(Window.unboundedPreceding, Window.currentRow))
    w_all = Window.partitionBy("user_id")
    return t.select(
        "user_id", "txn_id", "txn_date",
        F.sum("amount").over(w_run).alias("running_total"),
        F.sum("amount").over(w_all).alias("grand_total"),
    )
