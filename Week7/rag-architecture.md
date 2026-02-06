# RAG Architecture — Day 1 (Local Text RAG)

## Objective
The objective of Day 1 is to build the foundational layer of a Retrieval-Augmented Generation (RAG) system. This includes ingesting enterprise documents, converting them into semantic chunks, generating embeddings locally, storing them in a vector database, and enabling semantic retrieval.

At this stage, the system focuses only on retrieval. No answer generation using LLMs is performed.

---

## High-Level Flow
User Query → Retriever (FAISS) → Relevant Chunks (Context)

The retrieved context will later be passed to an LLM in subsequent days.

---

## Pipeline Components

### Data Ingestion
Raw markdown documents are stored in `src/data/raw/`.  
The ingestion pipeline reads these documents and prepares them for downstream processing.

File:
`src/pipelines/ingest.py`

---

### Text Cleaning
Before chunking, documents are lightly cleaned to:
- remove markdown symbols
- normalize whitespace
- preserve semantic meaning

This ensures model-friendly text without losing context.

---

### Chunking Strategy
Chunking is performed using token-based splitting to align with LLM token limits.

Parameters used:
- Chunk size: 700 tokens
- Overlap: 150 tokens

Token-based chunking is used instead of character-based chunking to avoid truncation issues and preserve semantic coherence.

Generated chunks are stored as JSON files in:
`src/data/chunks/`

Each chunk contains:
- chunk text
- chunk ID
- source metadata

---

### Embedding Generation
Each chunk is converted into a dense semantic vector using a local embedding model.

Model used:
`BAAI/bge-small-en`

File:
`src/embeddings/embedder.py`

Generated embeddings are stored in:
`src/data/embeddings/embeddings.json`

Each record includes:
- chunk text
- embedding vector
- metadata

---

### Vector Store (FAISS)
All embeddings are indexed using FAISS to enable efficient similarity search.

Index type:
`IndexFlatL2`

File:
`src/vectorstore/build_faiss.py`

Artifacts generated:
- FAISS index
- metadata mapping

Stored in:
`src/data/vectorstore/`

---

### Retriever Module
The retriever takes a user query and performs semantic search.

Steps:
1. Embed the user query using the same embedding model
2. Perform similarity search on the FAISS index
3. Retrieve top-K relevant chunks

File:
`src/retriever/query_engine.py`

This module outputs relevant context, not final answers.

---

## Folder Structure Overview

src/
pipelines/ingest.py
embeddings/embedder.py
vectorstore/build_faiss.py
retriever/query_engine.py
data/raw/
data/chunks/
data/embeddings/
data/vectorstore/

---

## Current Capabilities (Day 1)
- Local document ingestion
- Token-based chunking
- Local embedding generation
- FAISS vector indexing
- Semantic retrieval

---

## Scope Limitation
Day 1 does not include:
- LLM-based answer generation
- Hybrid retrieval
- Reranking
- Image RAG
- SQL question answering
- Evaluation or monitoring

These will be implemented in later days.

---

## Conclusion
This Day-1 architecture establishes a clean and scalable foundation for an enterprise-grade RAG system. The pipeline is modular, reproducible, and designed to support advanced retrieval and generation workflows in subsequent phases.
EOF
