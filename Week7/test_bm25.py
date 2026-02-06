from retriever.bm25_retriever import BM25Retriever

bm25 = BM25Retriever()

query = "credit underwriting"
results = bm25.search(query, top_k=5)

for r in results:
    print(r["metadata"]["source"])
    print(r["score"])
    print(r["text"][:200])
    print("-" * 40)
