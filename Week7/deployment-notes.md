# DEPLOYMENT-NOTES.md

## Week 7 – Enterprise GenAI System (Day 5 Capstone)

This document describes how to deploy, configure, and run the **Advanced RAG + Memory + Evaluation System** built as part of the Week 7 Launchpad capstone.
The system is designed to be **production-aligned**, **auditable**, and **enterprise-ready**.
Project Objectives

# The goal of this project is to demonstrate:

Retrieval-Augmented Generation (RAG)
Multimodal reasoning (Text + Image + Structured Data)
LLM-driven pipelines
Memory and self-evaluation
Hallucination detection
Production-style API design
---

## Supported Capabilities

The system supports the following APIs:

### 1. `/ask` – Text RAG
- Context-aware question answering
- Conversational memory (last 5 turns)
- Refinement loop
- Hallucination detection
- Confidence scoring
PI Endpoints (FastAPI)
Input

{
  "question": "What is RAG?",
  "context": "RAG retrieves documents before generating answers."
}

### 2. `/ask-image` – Multimodal Image RAG
- Image → Context retrieval (CLIP)
- OCR + Caption grounding
- Image → Text explanation
- Hallucination & faithfulness evaluation
Input

{
  "image_path": "src/data/images/report1/page_13_img_1.png",
  "question": "Explain what this diagram represents"
}

### 3. `/ask-sql` – SQL Question Answering
- Natural language → SQL using LLM
- Auto schema loading
- SQL validation
- Safe execution on SQLite
- Result summarization
Input

{
  "question": "Show total sales by artist for 2023"
}

---

## System Architecture

User query
   |
Retrieval(text/image/sql)
   |
LLM Answer generation
   |
Self Refinment
   |
Evaluation(Hallucination.Faithufulness,Confidence)
   |
Memory storage(last 5 messages)
   |
Structured API Response


---

## Tech Stack

- **LLMs**: Hosted APIs (Groq)
- **Embeddings**: SentenceTransformers (Text + CLIP)
- **Vector Search**: Cosine Similarity (Day-5 scope)
- **Image Retrieval**: CLIP (Image ↔ Text)
- **Database**: SQLite
- **API Framework**: FastAPI

---

## Environment Setup

### 1. Virtual Environment
```bash
source .venv/bin/activate

```




# 3. Conversational Memory (Day 5)

- Stores the last 5 interactions

- Logs questions, answers, and confidence scores

- Saved to CHAT-LOGS.json

- Key File

- src/memory/memory_store.py
CHAT-LOGS.json

# 4. Evaluation & Hallucination Detection

Each response is evaluated using heuristic metrics:

- Context match score
- Faithfulness score
- Hallucination flag
- Confidence score
- Short or weak contexts may yield strict (low) scores by design.

Key File
src/evaluation/rag_eval.py

# 5. Refinement Loop

If hallucination or low confidence is detected:

The system refines the answer using stricter grounding
Improves factual alignment
This mimics real-world RAG reliability workflows.
Deployment (FastAPI)
The system is exposed as a production-style FastAPI service.

## File

deployment/app.py

# Run Server
source .env
PYTHONPATH=src uvicorn deployment.app:app --reload

Swagger UI
http://127.0.0.1:8000/docs

## Configuration & Secrets

LLM API keys are never hardcoded
Environment variables are used:
GROQ_API_KEY
Config file

## Streamlit User Interface

A Streamlit-based UI was implemented to provide an interactive interface for the RAG system.

The UI supports:
- Text-based RAG queries
- Image-to-text explanation queries
- SQL Question Answering

The Streamlit app directly invokes the same backend pipelines used by the FastAPI service, ensuring consistency across API and UI layers.

Command to run:
source .env
PYTHONPATH=src streamlit run src/streamlit_app.py

## Deliverables Summary

✔ Text RAG Pipeline
✔ Multimodal Image RAG
✔ SQL-QA Engine
✔ Conversational Memory
✔ Self-reflection & Refinement
✔ Hallucination Detection
✔ Confidence Scoring
✔ FastAPI Deployment
✔ Production-style Folder Structure



