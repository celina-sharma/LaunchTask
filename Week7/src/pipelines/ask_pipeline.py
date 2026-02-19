# src/pipelines/ask_pipeline.py

from src.retriever.hybrid_retriever import HybridRetriever
from src.pipelines.context_builder import build_context_json
from src.generator.llm_answer import generate_answer
from src.evaluation.rag_eval import evaluate_answer
from src.memory.memory_store import save_interaction

CONFIDENCE_THRESHOLD = 0.4
retriever = HybridRetriever()


def format_context(context_json):
    sections = []
    for item in context_json["contexts"]:
        sections.append(
            f"[Source: {item['source']}]\n{item['text']}\n"
        )
    return "\n\n".join(sections)


def ask(question: str):

    # ---- Retrieval ----
    chunks = retriever.search(question)

    # ---- Build structured context ----
    context_json = build_context_json(chunks, question)

    # ---- Convert to string for LLM ----
    context_string = format_context(context_json)

    # ---- Generation ----
    answer = generate_answer(question, context_string)

    # ---- Evaluation ----
    eval_scores = evaluate_answer(question, context_string, answer)

    refined = False

    if eval_scores["hallucination"] or eval_scores["confidence"] < CONFIDENCE_THRESHOLD:
        critique_prompt = f"""
        Improve the following answer.
        Use ONLY the given context.
        Question: {question}
        Context: {context_string}
        Original Answer: {answer}
        """

        answer = generate_answer(critique_prompt, context_string)
        refined = True
        eval_scores = evaluate_answer(question, context_string, answer)

    # ---- Memory Save ----
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
        "evaluation": eval_scores,
        "context_used": context_json
    }
