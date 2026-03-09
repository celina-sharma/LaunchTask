# MEMORY-SYSTEM.md — Day 4: Memory Systems

## Overview
This document explains the memory system built in Day 4 which gives agents the ability to remember context, persist facts, and recall similar information using vector search.

---

## Memory Types

| Memory Type | File | Storage | Lifetime |
|---|---|---|---|
| Short-term | session_memory.py | Python list (RAM) | Current session only |
| Long-term | long_term.db | SQLite (disk) | Permanent |
| Vector | vector_store.py | FAISS (RAM) | Loaded per session |

---

## File Details

### 1. session_memory.py
- Stores conversation messages in current session
- Keeps last 10 messages
- Summarizes important facts using Mistral
- Saves facts to long_term.db per user

### 2. vector_store.py
- Converts facts to embeddings using sentence-transformers (all-MiniLM-L6-v2)
- Stores embeddings in FAISS IndexFlatL2
- Searches for similar context when new query comes in
- Loads only specific user's facts from long_term.db

### 3. long_term.db
- SQLite database for persistent memory
- Stores facts per user_id
- Survives across sessions
- Schema:
```sql
CREATE TABLE long_term_memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    fact TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

---

## Pipeline Flow
```
New Query
→ Search memory (FAISS + session memory)
→ Fetch similar context
→ Inject in prompt
→ Generate with context (Mistral)
```

---

## How Memory Works Together
```
User starts conversation
        ↓
Load user's facts from long_term.db → FAISS
        ↓
User sends message
        ↓
Search FAISS for similar context
Search session memory for current conversation
        ↓
Combine both contexts
        ↓
Inject into Mistral prompt
        ↓
Generate response with memory context
        ↓
Store message in session memory
        ↓
User types 'quit'
        ↓
Summarize facts using Mistral
        ↓
Save facts to long_term.db (per user_id)
        ↓
Store facts in FAISS
```

---

## User ID System

Each user has their own memory space:
- Facts saved with `user_id` in long_term.db
- On login, only that user's facts loaded into FAISS
- No mixing of different users' data

---

## Episodic vs Semantic Memory

| Type | Description | In our system |
|---|---|---|
| Episodic | Specific events/conversations | Session memory (current conversation) |
| Semantic | General facts about user | long_term.db + FAISS |

---

## Model Used
- **Mistral** via Ollama — for fact summarization and response generation
- **all-MiniLM-L6-v2** — for converting text to embeddings (384 dimensions)
- **FAISS IndexFlatL2** — for similarity search

---

## Files
```
Day4/
├── memory/
│   ├── session_memory.py   # Short-term memory + fact summarization
│   ├── vector_store.py     # FAISS vector memory
│   └── long_term.db        # SQLite persistent memory
├── main_pipeline.py        # Full memory pipeline
└── MEMORY-SYSTEM.md        # This file
```