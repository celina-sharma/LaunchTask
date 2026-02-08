from retriever.image_retriever import ImageRetriever
from generator.llm_answer import generate_answer
from evaluation.rag_eval import evaluate_answer
from memory.memory_store import save_interaction


def ask_image(image_path: str, question: str):
    retriever = ImageRetriever()

    #retrieve similar images
    results = retriever.search_by_image(image_path, top_k=3)
    top_image = results[0]

    context = ""
    for r in results:
        context += f"""
    Caption: {r.get('caption','')}
    OCR: {r.get('ocr_text','')}
    """


    answer = generate_answer(question, context, mode="image")


    evaluation = evaluate_answer(question, context, answer)

    save_interaction(
        endpoint="/ask-image",
        question=question,
        answer=answer,
        confidence=evaluation["confidence"]
    )

    return {
        "image": top_image["image_path"],
        "answer": answer,
        "evaluation": evaluation
    }
