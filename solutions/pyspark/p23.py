# p23 self-join for pairs; emp_id1 < emp_id2 removes self-pairs and mirrors.
from typing import Dict
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def solve(spark: SparkSession, dfs: Dict[str, DataFrame]) -> DataFrame:
    a = dfs["employees"].alias("a")
    b = dfs["employees"].alias("b")
    return (a.join(b, (F.col("a.dept") == F.col("b.dept")) &
                      (F.col("a.emp_id") < F.col("b.emp_id")))
            .select(F.col("a.emp_id").alias("emp_id1"),
                    F.col("b.emp_id").alias("emp_id2"),
                    F.col("a.dept").alias("dept")))
