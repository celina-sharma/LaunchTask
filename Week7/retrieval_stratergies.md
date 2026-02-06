# Retrieval Strategies — Week 7 (Day 2)

## Overview

This system implements **advanced retrieval strategies** to improve both
**recall** (finding all relevant information) and **precision** (ranking the best results first)
for an enterprise-grade RAG (Retrieval-Augmented Generation) pipeline.

The retrieval stack is designed to minimize hallucination and maximize answer faithfulness.

---

## Retrieval Architecture (High Level)

User Query
↓
Hybrid Retrieval
(BM25 + Semantic Search)
↓
Deduplication
↓
Reranking (Cross-Encoder)
↓
MMR (Diversity Control)
↓
Context Builder
↓
LLM

---

## 1. Semantic Retrieval (Vector Search)

### What it is
Semantic retrieval uses **dense vector embeddings** to find meaning-based similarities
between the user query and document chunks.

### Implementation
- Model: `BAAI/bge-small-en`
- Vector DB: FAISS
- Similarity metric: Inner Product (IP)
- Embeddings normalized for cosine similarity

### Why it’s needed
- Handles paraphrases
- Understands semantic intent, not just keywords
- Works even when query words don’t exactly appear in the document

### Limitation
- Can miss exact terms (names, codes, acronyms)
- Can retrieve semantically similar but irrelevant chunks

---

## 2. Keyword Retrieval (BM25)

### What it is
BM25 is a **lexical (term-based)** retrieval algorithm that ranks documents based on exact word matches.

### Implementation
- Library: `rank-bm25`
- Token-based keyword scoring

### Why it’s needed
- Excellent for:
  - Domain keywords
  - Legal terms
  - Financial terminology
  - IDs, codes, acronyms
- Complements semantic search

### Limitation
- Fails when synonyms or paraphrases are used

---

## 3. Hybrid Retrieval (Semantic + Keyword)

### What it is
Hybrid retrieval combines **semantic search + BM25 keyword search**.

### Implementation
- Both retrievals are executed independently
- Results are merged
- Deduplication is applied based on chunk text
- Retrieval provenance is preserved:
  - `semantic`
  - `keyword`
  - `semantic+keyword`

### Why it’s critical
- Increases recall
- Prevents missing important facts
- Enterprise-standard approach

---

## 4. Deduplication Strategy

### What it is
Removes duplicate chunks retrieved by multiple strategies.

### Implementation
- Hash-based deduplication on normalized chunk text
- Keeps provenance information

### Benefit
- Avoids repeated context
- Saves LLM context window
- Improves response clarity

---

## 5. Reranking (Cross-Encoder)

### What it is
A **Cross-Encoder** jointly evaluates `(query, chunk)` pairs
to compute precise relevance scores.

### Implementation
- Model: `cross-encoder/ms-marco-MiniLM-L-6-v2`
- Input: Candidate chunks from hybrid retrieval
- Output: Reranked chunks with `rerank_score`

### Why it’s important
- Fixes rough ordering from retrieval stage
- Strongly improves precision
- Reduces hallucination risk

### Tradeoff
- Slower than vector search
- Used only on top-N candidates

---

## 6. Max Marginal Relevance (MMR)

### What it is
MMR balances:
- **Relevance** to the query
- **Diversity** among retrieved chunks

### Formula
MMR = λ * similarity(query, doc)
     − (1 − λ) * similarity(doc, selected_docs)

### Implementation
- Uses cosine similarity on embeddings
- λ (lambda) controls relevance vs diversity

### Why it’s needed
- Prevents redundant chunks
- Ensures coverage of different aspects of the answer
- Essential for long enterprise documents

---

## 7. Context Construction

### What it is
Final step that prepares retrieved information for LLM input.

### Implementation
- Structured JSON context
- Character-limited (context window safe)
- Includes:
  - Chunk ID
  - Source document
  - Retrieval method
  - Clean text preview

### Benefit
- Traceable answers
- Audit-ready output
- Prevents prompt overflow

---

## Final Result

This retrieval pipeline achieves:
- High recall via hybrid search
- High precision via reranking
- Reduced redundancy via MMR
- Faithful, traceable, enterprise-grade context for LLMs

---

## Status

✔ Hybrid Retrieval  
✔ Deduplication  
✔ Reranking  
✔ MMR  
✔ Context Optimization  

