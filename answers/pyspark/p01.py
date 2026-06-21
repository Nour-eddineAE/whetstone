# p01 [joins/easy]
# Implement solve(spark, dfs) -> DataFrame. Expected columns: emp_id, name, dept_id
# dfs keys: employees, departments, events, transactions, user_tags
from pyspark.sql.functions import col
from pyspark.sql.window import Window


def solve(spark, dfs):
    # TODO: replace with your solution
    return dfs["employees"].join(dfs["departments"], col("dept").is_equal_to("dept_name"))