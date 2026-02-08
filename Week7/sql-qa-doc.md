# SQL-QA Engine — Day 4 (Week 7)

This module implements a **Natural Language to SQL Question Answering (SQL-QA) Engine** as part of Week 7 Day 4. The system allows users to ask analytical questions in plain English and retrieves answers by generating, validating, and executing SQL queries on a relational database.

The primary objective of this task is to demonstrate **LLM-driven structured querying with safety, schema-awareness, and execution validation**.

---

## Example Query

**User Input**
User Question
↓
LLM-based SQL Generation
↓
Schema-aware SQL Validation
↓
Injection-safe SQL Execution
↓
Result Summarization


---

## Core Components

### SQL Generation Using LLM

The SQL is generated dynamically using a hosted Large Language Model.

**File:**  
`src/generator/sql_generator.py`

Key characteristics:
- SQL is **not hardcoded**
- Database schema is injected into the LLM prompt
- Relationships between tables are explicitly defined
- The LLM is instructed to:
  - Use only schema-valid tables and columns
  - Generate correct joins (`sales → albums → artists`)
  - Apply grouping logic when the query contains phrases like *"by artist"*
  - Return only raw SQL (no markdown, no explanations)

This ensures schema-grounded, realistic SQL generation.

---

### Automatic Schema Loader

**File:**  
`src/utils/schema_loader.py`

This utility:
- Reads the SQLite database schema at runtime
- Extracts tables and columns
- Feeds schema information into the SQL generation prompt

As a result, the LLM does not hallucinate columns or tables and respects the actual database structure.

---

### SQL Validation and Injection Safety

**File:**  
`src/utils/sql_validator.py`

Before execution, generated SQL is validated to ensure safety:
- Dangerous SQL operations are blocked:
  - `DROP`
  - `DELETE`
  - `UPDATE`
  - `ALTER`
- Only safe, read-only SQL queries proceed to execution

This step prevents accidental or malicious database modification.

---

### SQL Execution Engine

**File:**  
`src/utils/sql_executor.py`

Responsibilities:
- Executes validated SQL queries on the SQLite database
- Handles execution errors safely
- Returns results in a structured format

This component acts as the secure interface between the LLM-generated query and the database.

---

### Result Summarization

**File:**  
`src/utils/result_summarizer.py`

This step converts raw SQL results into clean, structured Python objects:
- SQL rows are mapped to dictionaries
- Output is suitable for APIs, analytics layers, or RAG pipelines.

---

### SQL-QA Pipeline

**File:**  
`src/pipelines/sql_pipeline.py`

This pipeline orchestrates the complete flow:
1. Accepts a natural language question
2. Generates SQL using the LLM
3. Validates and sanitizes the SQL
4. Executes the query on SQLite
5. Summarizes and returns results

The pipeline provides a single entry point:



---

## Sample Output

```json
{
  "question": "Show total sales by artist for 2023",
  "sql": "SELECT artists.name, SUM(sales.amount) FROM ... GROUP BY artists.name",
  "result": [
    { "name": "Adele", "SUM(sales.amount)": 150000 },
    { "name": "Taylor Swift", "SUM(sales.amount)": 210000 },
    { "name": "The Weeknd", "SUM(sales.amount)": 178000 }
  ]
}

--- 

**Features Implemented**

1. LLM-driven SQL generation
2. Automatic database schema loading
3. Schema-aware query construction
4. SQLite database support

---


