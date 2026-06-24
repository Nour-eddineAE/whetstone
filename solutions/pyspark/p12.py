# p12 second highest salary. Find the max, then the max strictly below it.
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def solve(spark: SparkSession, employees: DataFrame) -> DataFrame:
    e = employees
    top = e.agg(F.max("salary")).first()[0]
    return (e.where(F.col("salary") < top)
            .agg(F.max("salary").alias("second_highest")))
