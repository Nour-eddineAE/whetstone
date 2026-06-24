# p01 inner join: employees whose dept matches a department row.
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def solve(spark: SparkSession, employees: DataFrame, departments: DataFrame) -> DataFrame:
    e, d = employees, departments
    # join key: employees.dept == departments.dept_name. 'inner' drops unmatched.
    return (e.join(d, e.dept == d.dept_name, "inner")
            .select(e.emp_id, e.name, d.dept_id))
