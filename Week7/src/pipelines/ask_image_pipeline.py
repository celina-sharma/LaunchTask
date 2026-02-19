from retriever.image_retriever import ImageRetriever
from generator.llm_answer import generate_answer
from evaluation.rag_eval import evaluate_answer
from memory.memory_store import save_interaction


def ask_image(question: str):

    retriever = ImageRetriever()

    # Combine question-based search for relevance
    results = retriever.search(question, top_k=3)

    context_blocks = []

    for i, r in enumerate(results, 1):
        block = f"""
Image {i}:
Source: {r.get('source_pdf')}
Page: {r.get('page')}
Caption: {r.get('caption','')}
OCR Extracted Text:
{r.get('ocr_text','')}
"""
        context_blocks.append(block)

    context = "\n\n".join(context_blocks)

    answer = generate_answer(question, context, mode="image")

    evaluation = evaluate_answer(question, context, answer)

    save_interaction(
        endpoint="/ask-image",
        question=question,
        answer=answer,
        confidence=evaluation["confidence"]
    )

    return {
        "answer": answer,
        "evaluation": evaluation,
        "retrieved_images": [r["image_path"] for r in results]
    }
