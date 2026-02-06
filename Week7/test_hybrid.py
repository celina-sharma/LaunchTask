import json
import numpy as np

from retriever.hybrid_retriever import HybridRetriever
from retriever.reranker import Reranker
from retriever.mmr import mmr
from pipelines.context_builder import build_context_json
from utils.embedding_model import get_embedding_model


query = "credit underwriting risk assessment loan evaluation"

# ✅ Load shared embedding model ONCE
embed_model = get_embedding_model()

# ---------------- HYBRID RETRIEVAL ----------------
retriever = HybridRetriever(
    semantic_k=15,
    keyword_k=15
)

candidates = retriever.search(query)
print(f"[INFO] Candidates after hybrid retrieval: {len(candidates)}")

# ---------------- RERANKING ----------------
reranker = Reranker(top_k=10)
reranked = reranker.rerank(query, candidates)
print(f"[INFO] Candidates after reranking: {len(reranked)}")

# ---------------- MMR ----------------
query_embedding = embed_model.encode(
    query,
    normalize_embeddings=True
)

doc_embeddings = np.array(
    [c["embedding"] for c in reranked],
    dtype="float32"
)

final_results = mmr(
    query_embedding=query_embedding,
    doc_embeddings=doc_embeddings,
    documents=reranked,
    top_k=5
)

# ---------------- CONTEXT BUILDING ----------------
context_json = build_context_json(
    final_results,
    query=query,
    max_chars=6000
)

print("\nFINAL CONTEXT (JSON FORMAT)\n")
print(json.dumps(context_json, indent=2))
