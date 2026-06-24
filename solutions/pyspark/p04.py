# p04 semi-join: employees with >=1 transaction, no row multiplication.
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def solve(spark: SparkSession, employees: DataFrame, transactions: DataFrame) -> DataFrame:
    e, t = employees, transactions
    # left_semi keeps left rows that have a match, emits no right columns, no dups.
    return e.join(t, e.emp_id == t.user_id, "left_semi").select("emp_id", "name")
