from utils.llm_client import call_llm


def generate_answer(question: str, context: str, mode: str = "text"):
    
    if mode == "image":
        prompt = f"""
You are an analytical assistant working with extracted image data.

You MUST use ONLY the provided OCR text and captions as your source of truth.

STRICT RULES:
- Do NOT invent facts.
- Do NOT assume missing numbers.
- Do NOT round values.
- If something is unclear or unreadable, say: "Not clearly readable".
- If multiple images are provided, treat all as possible evidence.
- If the question requires comparison, extract exact values first, then compare numerically.
- If the question is descriptive, summarize strictly from visible information only.
- Do NOT generate SQL.
- Do NOT generate code.

When numbers are involved:
1. List exact values exactly as written.
2. Then perform comparison logically.
3. Then provide the final conclusion clearly.

If the answer cannot be determined from the text, clearly say:
"Insufficient information in retrieved images."

Image Context:
{context}

User Question:
{question}

Answer:
"""

    else:
        # TEXT RAG MODE
        prompt = f"""
You are a factual assistant.

You MUST answer ONLY using the provided context.
If the answer is not present in the context, say:
"Insufficient information in context."

Rules:
- Be concise.
- Do NOT invent facts.
- Do NOT use external knowledge.
- Do NOT generate SQL.
- Do NOT generate code.

Context:
{context}

Question:
{question}

Answer:
"""

    return call_llm(prompt)
