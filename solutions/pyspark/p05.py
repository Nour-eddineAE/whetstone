# p05 revenue per dept. Join ONE child (transactions) then aggregate.
# Joining events too would fan-out and inflate the sum.
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def solve(spark: SparkSession, employees: DataFrame, transactions: DataFrame) -> DataFrame:
    e, t = employees, transactions
    return (e.join(t, e.emp_id == t.user_id)
            .groupBy("dept")
            .agg(F.sum("amount").alias("total_amount")))
