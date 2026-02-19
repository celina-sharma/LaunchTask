from src.pipelines.sql_pipeline import run_sql_pipeline

result = run_sql_pipeline("Show total sales by artist for 2023")

print("\nGenerated SQL:\n")
print(result["sql"])

print("\nResult:\n")
print(result["result"])
