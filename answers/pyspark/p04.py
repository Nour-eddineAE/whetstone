# p04 [joins/med]
# Implement solve(spark, employees, transactions) -> DataFrame. Expected columns: emp_id, name
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def solve(spark: SparkSession, employees: DataFrame, transactions: DataFrame) -> DataFrame:
    return employees \
			.join(transactions, on=employees["emp_id"] == transactions["user_id"], how="leftsemi") \
			.select("emp_id", "name")