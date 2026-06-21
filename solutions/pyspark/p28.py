# p28 native Spark pivot: groupBy the row key, pivot the column key (with an
# explicit value list to fix column order), aggregate, fill missing cells with 0.
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def solve(spark, dfs):
    types = ["view", "signup", "purchase", "click", "login"]
    return (dfs["events"].groupBy("user_id")
            .pivot("event_type", types)
            .count()
            .na.fill(0)
            .select("user_id", *types))
