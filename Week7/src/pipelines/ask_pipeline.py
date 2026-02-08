# src/pipelines/ask_pipeline.py

from evaluation.rag_eval import evaluate_answer
from memory.memory_store import save_interaction, get_recent_memory
from generator.llm_answer import generate_answer   # text RAG answer

CONFIDENCE_THRESHOLD = 0.4

def ask(question: str, context: str):
    # 1. initial answer
    answer = generate_answer(question, context)

    # 2. evaluate
    eval_scores = evaluate_answer(question, context, answer)

    refined = False

    # 3. refinement loop (single pass)
    if eval_scores["hallucination"] or eval_scores["confidence"] < CONFIDENCE_THRESHOLD:
        critique_prompt = f"""
        Improve the following answer.
        Use ONLY the given context.
        Question: {question}
        Context: {context}
        Original Answer: {answer}
        """

        answer = generate_answer(critique_prompt, context)
        refined = True

        # re-evaluate after refinement
        eval_scores = evaluate_answer(question, context, answer)

    # 4. save memory
    save_interaction(
        endpoint="/ask",
        question=question,
        answer=answer,
        confidence=eval_scores["confidence"]
    )

    return {
        "question": question,
        "answer": answer,
        "refined": refined,
        "evaluation": eval_scores
    }
