# p02 [joins/easy]
# Implement solve(spark, employees, departments) -> DataFrame. Expected columns: emp_id, name, dept_id
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def solve(spark: SparkSession, employees: DataFrame, departments: DataFrame) -> DataFrame:
    # TODO: replace with your solution
    return employees.join(departments, employees["dept"] == departments["dept_name"], how = "left").select("emp_id", "name", "dept_id") 