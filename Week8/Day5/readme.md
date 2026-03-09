# Day 5 — Local LLM API

## What is this?
A local LLM API server built with FastAPI and TinyLlama GGUF model.
It has a Streamlit UI for chatting with the model.

---

## Project Structure
```
Day5/
├── deploy/
│   ├── app.py            ← FastAPI server
│   ├── model_loader.py   ← loads GGUF model
│   ├── config.py         ← settings
│   └── streamlit_app.py  ← Streamlit UI
├── README.md
├── DOCKERFILE
└── FINAL-REPORT.md
```

---

## Requirements
- Python 3.12
- TinyLlama GGUF model (from Day 3)

---

## Installation
```bash
pip install fastapi uvicorn llama-cpp-python streamlit requests
```

---

## How to Run

### Step 1 — Start FastAPI server:
```bash
cd Day5/deploy
uvicorn app:app --reload
```
Server runs on: http://localhost:8000

### Step 2 — Start Streamlit UI:
```bash
cd Day5/deploy
streamlit run streamlit.py
```
UI runs on: http://localhost:8501

---

## API Endpoints

### POST /generate
Single prompt → single response

Example:
```json
{
  "prompt": "Write a Python function to add two numbers",
  "max_tokens": 200,
  "temperature": 0.7,
  "top_k": 40,
  "top_p": 0.95
}
```

### POST /chat
Multi-turn conversation with history

Example:
```json
{
  "messages": [
    {"role": "user", "content": "Write a Python function to add two numbers"}
  ],
  "system_prompt": "You are a helpful assistant.",
  "max_tokens": 200,
  "temperature": 0.7,
  "top_k": 40,
  "top_p": 0.95
}
```

---

## Features
- Uses quantized GGUF model (TinyLlama 1.1B)
- Infinite chat mode with history
- System + user prompts
- Top-k, top-p, temperature controls
- Logs + request ID for every request
- Keyword filter — only answers coding/AI questions
- Ready for RAG and Agents

---

## Docker
```bash
docker build -t local-llm-api .
docker run -p 8000:8000 local-llm-api
```