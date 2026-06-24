# p05 [joins/med]
# Implement solve(spark, employees, transactions) -> DataFrame. Expected columns: dept, total_amount

def solve(spark: SparkSession, employees: DataFrame, transactions: DataFrame) -> DataFrame:
    return employees.join(transactions, on=employees["emp_id"] == transactions["user_id"], how="left") \
    			.groupBy("dept") \
    			.agg(sum("amount").alias("total_amount")) \
    			.select("dept", "total_amount") \
				.filter(col("total_amount").isNotNull()) \




   




