# p26 derive a YYYY-MM month key, then group by it.
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def solve(spark: SparkSession, transactions: DataFrame) -> DataFrame:
    t = transactions.withColumn("month", F.date_format("txn_date", "yyyy-MM"))
    return t.groupBy("month").agg(
        F.count(F.lit(1)).alias("txn_count"),
        F.sum("amount").alias("total_amount"),
    )
