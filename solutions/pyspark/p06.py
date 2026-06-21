# p06 top earner per dept via row_number, deterministic emp_id tiebreak.
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def solve(spark, dfs):
    e = dfs["employees"]
    w = Window.partitionBy("dept").orderBy(F.col("salary").desc(), F.col("emp_id"))
    return (e.withColumn("rn", F.row_number().over(w))
            .where(F.col("rn") == 1)
            .select("dept", "emp_id", "name", "salary"))
