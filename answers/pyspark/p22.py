# p22 [joins/med]
# Implement solve(spark, employees) -> DataFrame. Expected columns: emp_id, name, salary, manager_salary


def solve(spark: SparkSession, employees: DataFrame) -> DataFrame:
    managers = employees.alias("mgr")
    emps = employees.alias("emp")
	
    return emps.join(managers, col("emp.manager_id") == col("mgr.emp_id"), how="inner") \
				.filter(col("emp.salary")> col("mgr.salary")) \
				.select(col("emp.emp_id"), col("emp.name"), col("emp.salary"), col("mgr.salary").alias("manager_salary"))