# p07 [window/med]
# Implement solve(spark, employees) -> DataFrame. Expected columns: emp_id, dept, salary, rnk, dense_rnk


def solve(spark: SparkSession, employees: DataFrame) -> DataFrame:
    rnkWindow = Window.partitionBy("dept").orderBy(col("salary").desc())
    
    return employees \
			.withColumn("rnk", rank().over(rnkWindow)) \
			.withColumn("dense_rnk", dense_rank().over(rnkWindow)) \
			.select("emp_id", "dept", "salary", "rnk", "dense_rnk")
