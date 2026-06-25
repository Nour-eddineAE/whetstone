# p08 [window/med]
# Implement solve(spark, employees) -> DataFrame. Expected columns: dept, emp_id, name, salary, rn


def solve(spark: SparkSession, employees: DataFrame) -> DataFrame:
    rnWindow = Window.partitionBy("dept").orderBy(col("salary").desc(), col("emp_id"))
    
    return employees.withColumn("rn", rank().over(rnWindow)) \
					.filter(col("rn") <= 2) \
					.select("dept", "emp_id", "name", "salary", "rn")