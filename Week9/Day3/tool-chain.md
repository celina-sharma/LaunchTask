# TOOL-CHAIN.md — Day 3: Tool-Calling Agents

## Overview
This document explains the tool-calling agents built in Day 3 and how they work together in a pipeline.

---

## Agents and Tools

| Agent | Tool | Purpose |
|---|---|---|
| Code Agent | Python execution | Executes Python code and returns output |
| DB Agent | SQLite + SQL | Queries SQLite database and returns results |
| File Agent | Read/write .txt, .csv | Reads CSV files and writes TXT files |

---

## Agent Details

### 1. Code Agent
- **File**: `/tools/code_executor.py`
- **Tool**: `run_python_code`
- **How it works**: Receives Python code as input, executes it using subprocess, returns output or error
- **Use case**: Data analysis, calculations, generating insights

### 2. DB Agent
- **File**: `/tools/db_agent.py`
- **Tool**: `query_database`
- **How it works**: Receives SQL query as input, executes it on sales.db, returns columns and results
- **Database**: `sales.db` created from `sales.csv`
- **Use case**: Querying sales data by region, product, payment method

### 3. File Agent
- **File**: `/tools/file_agent.py`
- **Tools**: `read_csv`, `write_txt`
- **How it works**: Reads CSV files and returns contents, writes content to TXT files
- **Use case**: Reading sales.csv, saving insights to insights.txt

---

## Pipeline Flow
```
User: "Analyze sales.csv and generate top 5 insights"
        ↓
Orchestrator
- Receives user request
- Plans tasks for agents
        ↓
File Agent
- Reads sales.csv
- Returns column names and row count
        ↓
Code Agent
- Reads sales.csv using pandas
- Generates top 5 insights
        ↓
File Agent
- Saves insights to insights.txt
        ↓
Combined Final Answer
```

---

## Data Flow
```
sales.csv → File Agent → reads file
sales.csv → DB Agent → imports into sales.db → queries with SQL
sales.csv → Code Agent → reads with pandas → generates insights
insights → File Agent → saves to insights.txt
```

---

## Tool Registration

All tools are registered in `main_pipeline_day3.py`:
```python
autogen.register_function(read_csv, caller=file_agent, executor=user_proxy)
autogen.register_function(write_txt, caller=file_agent, executor=user_proxy)
autogen.register_function(run_python_code, caller=code_agent, executor=user_proxy)
autogen.register_function(query_database, caller=db_agent, executor=user_proxy)
```

---

## Key Concepts

- **Tool Calling**: Agent decides when to use a tool and what arguments to pass
- **Function Calling**: Python function is registered as a tool for the agent
- **Caller**: Agent that decides to use the tool
- **Executor**: Agent that actually runs the tool
- **System-to-tool execution**: Agent uses tools to interact with external systems

---

## Model Used
- **Mistral** via Ollama (local, CPU-only)
- Mistral supports tool calling unlike Phi-3