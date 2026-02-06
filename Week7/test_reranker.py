from retriever.hybrid_retriever import HybridRetriever
from retriever.reranker import Reranker

query = "credit underwriting risk assessment"

retriever = HybridRetriever(semantic_k=15, keyword_k=15)
candidates = retriever.search(query)

print(f"Candidates fetched: {len(candidates)}")

#Rerank the candidates
reranker = Reranker(top_k=5)
results = reranker.rerank(query, candidates)

#Inspect results
for i, r in enumerate(results, 1):
    print(i, r["rerank_score"])
    print(r["metadata"]["source"])
    print(r["text"][:200])
    print("-" * 60)
