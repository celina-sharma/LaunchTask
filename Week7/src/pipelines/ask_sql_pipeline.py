from generator.sql_generator import generate_sql
from utils.sql_validator import validate_sql
from utils.sql_executor import execute_sql
from utils.result_summarizer import summarize_result
from evaluation.rag_eval import evaluate_answer
from memory.memory_store import save_interaction


def ask_sql(question: str):

    sql = generate_sql(question)

    validate_sql(sql)

    results = execute_sql(sql)

    summary = summarize_result(results)
    
    evaluation = evaluate_answer(
        question=question,
        context=str(results),
        answer=str(summary)
    )

    save_interaction(
        endpoint="/ask-sql",
        question=question,
        answer=str(summary),
        confidence=evaluation["confidence"]
    )

    return {
        "question": question,
        "sql": sql,
        "result": summary,
        "evaluation": evaluation
    }
