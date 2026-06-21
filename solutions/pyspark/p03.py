# p03 anti-join: leaf employees (never appear as a manager_id).
# left_anti is the NULL-safe equivalent of NOT IN / NOT EXISTS.
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def solve(spark, dfs):
    e = dfs["employees"]
    managers = (e.select(F.col("manager_id").alias("mid"))
                .where(F.col("mid").isNotNull())
                .distinct())
    return (e.join(managers, e.emp_id == managers.mid, "left_anti")
            .select("emp_id", "name"))
