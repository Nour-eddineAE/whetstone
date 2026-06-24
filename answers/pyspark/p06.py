# p06 [window/easy]
# Implement solve(spark, employees) -> DataFrame. Expected columns: dept, emp_id, name, salary


def solve(spark: SparkSession, employees: DataFrame) -> DataFrame:
    rnWindow = Window.partitionBy("dept") \
    				.orderBy(col("salary").desc(), col("emp_id"))
    
    return employees \
			.withColumn("rn", row_number().over(rnWindow)) \
			.filter(col("rn") == 1)\
    		.select("dept", "emp_id", "name", "salary")
    		
    
    
    