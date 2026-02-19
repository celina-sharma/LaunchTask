from generator.sql_generator import generate_sql
from utils.sql_validator import validate_sql
from utils.sql_executor import execute_sql
from utils.result_summarizer import summarize_result

def run_sql_pipeline(question: str):
    sql = generate_sql(question)
    print("Generated SQL:", sql)
    sql = validate_sql(sql) 
    results = execute_sql(sql)
    summary = summarize_result(results)

    return {
        "question": question,
        "sql": sql,
        "result": summary
    }

