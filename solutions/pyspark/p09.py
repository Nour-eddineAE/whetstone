# p09 running total per user. rowsBetween(unboundedPreceding, currentRow) = cumulative.
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def solve(spark: SparkSession, transactions: DataFrame) -> DataFrame:
    t = transactions
    w = (Window.partitionBy("user_id").orderBy("txn_date", "txn_id")
         .rowsBetween(Window.unboundedPreceding, Window.currentRow))
    return t.select(
        "user_id", "txn_id", "txn_date", "amount",
        F.sum("amount").over(w).alias("running_total"),
    )
