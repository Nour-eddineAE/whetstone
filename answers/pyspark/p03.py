# p03 [joins/med]
# Implement solve(spark, employees) -> DataFrame. Expected columns: emp_id, name
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def solve(spark: SparkSession, employees: DataFrame) -> DataFrame:
    managers_ids = employees.select(F.col("manager_id").alias("mgr_id")) \
    					.filter(F.col("mgr_id").isNotNull()) \
    					.distinct()

    return employees \
			.join(managers_ids, employees["emp_id"] == managers_ids["mgr_id"], how="leftanti") \
			.select("emp_id", "name") 