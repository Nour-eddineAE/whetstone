# p05 revenue per dept. Join ONE child (transactions) then aggregate.
# Joining events too would fan-out and inflate the sum.
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def solve(spark, dfs):
    e, t = dfs["employees"], dfs["transactions"]
    return (e.join(t, e.emp_id == t.user_id)
            .groupBy("dept")
            .agg(F.sum("amount").alias("total_amount")))
