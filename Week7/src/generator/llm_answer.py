from utils.llm_client import call_llm


def generate_answer(question: str, context: str, mode: str = "text"):
    if mode == "image":
        prompt = f"""
You are an expert analyst.

Task:
Explain the image in plain English using ONLY the provided information.

Rules:
- Do NOT generate SQL
- Do NOT generate code
- Do NOT invent new facts
- If information is missing, say so clearly

Image context:
{context}

User question:
{question}

Answer:
"""
    else:
        prompt = f"""
Answer the question using the context below.
Be concise, factual, and grounded in the context.

Context:
{context}

Question:
{question}

Answer:
"""

    return call_llm(prompt)
