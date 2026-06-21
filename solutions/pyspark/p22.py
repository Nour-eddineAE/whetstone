# p22 self-join: alias the same DataFrame twice so the join keys are unambiguous.
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def solve(spark, dfs):
    e = dfs["employees"].alias("e")
    m = dfs["employees"].alias("m")
    return (e.join(m, F.col("e.manager_id") == F.col("m.emp_id"))
            .where(F.col("e.salary") > F.col("m.salary"))
            .select(F.col("e.emp_id"), F.col("e.name"), F.col("e.salary"),
                    F.col("m.salary").alias("manager_salary")))
