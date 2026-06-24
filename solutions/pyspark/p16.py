# p16 median per user. expr('percentile(amount, 0.5)') is the exact interpolated
# median (matches DuckDB's median()). percentile_approx would only approximate.
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def solve(spark: SparkSession, transactions: DataFrame) -> DataFrame:
    t = transactions
    return (t.groupBy("user_id")
            .agg(F.expr("percentile(amount, 0.5)").alias("median_amount")))
