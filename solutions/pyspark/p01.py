# p01 inner join: employees whose dept matches a department row.
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def solve(spark, dfs):
    e, d = dfs["employees"], dfs["departments"]
    # join key: employees.dept == departments.dept_name. 'inner' drops unmatched.
    return (e.join(d, e.dept == d.dept_name, "inner")
            .select(e.emp_id, e.name, d.dept_id))
