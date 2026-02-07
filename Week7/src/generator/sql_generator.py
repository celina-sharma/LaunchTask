from utils.schema_loader import load_db_schema
from utils.llm_client import call_llm


def generate_sql(question: str) -> str:
    """
    Generate SQL from natural language using an LLM.
    The SQL must be schema-aware and safe to execute.
    """

    schema = load_db_schema()

    prompt = f"""
You are an expert SQL generator.

Database schema:
{schema}

Rules you MUST follow:
- Use ONLY tables and columns that exist in the schema
- sales links to albums using sales.album_id
- albums links to artists using albums.artist_id
- Artist names are stored in artists.name
- If the question contains the phrase "by artist":
  - You MUST select artists.name
  - You MUST GROUP BY artists.name
- Do NOT invent columns
- Do NOT use aliases incorrectly
- Do NOT include explanations
- Do NOT use markdown or code fences
- Return ONLY valid raw SQL

User question:
{question}

SQL:
"""

    sql = call_llm(prompt)
    return sql.strip()
