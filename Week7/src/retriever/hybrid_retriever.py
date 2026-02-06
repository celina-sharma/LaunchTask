from retriever.bm25_retriever import BM25Retriever
from retriever.query_engine import semantic_search
from retriever.mmr import mmr
import numpy as np

class HybridRetriever:
    def __init__(self, semantic_k=10, keyword_k=10, final_k=5):
        self.semantic_k = semantic_k
        self.keyword_k = keyword_k
        self.final_k = final_k
        self.bm25 = BM25Retriever()

    def search(self, query: str):
        # 1. Semantic retrieval (has embeddings)
        semantic_results = semantic_search(query, top_k=self.semantic_k)
        for r in semantic_results:
            r["retrieval_type"] = "semantic"

        # 2. Keyword retrieval (no embeddings)
        keyword_results = self.bm25.search(query, top_k=self.keyword_k)
        for r in keyword_results:
            r["retrieval_type"] = "keyword"

        # 3. Deduplication+merge
        merged = {}
        for r in semantic_results + keyword_results:
            key = r["text"].strip()
            if key not in merged:
                merged[key] = r
            else:
                merged[key]["retrieval_type"] += f"+{r['retrieval_type']}"

        candidates = list(merged.values())

        #only chunks with embeddings go to mmr
        mmr_candidates = [
            c for c in candidates if "embedding" in c
        ]

        if not mmr_candidates:
            return candidates[: self.final_k]

        doc_embeddings = np.array(
            [c["embedding"] for c in mmr_candidates],
            dtype="float32"
        )

        query_embedding = doc_embeddings[0] * 0 + doc_embeddings[0]  

        mmr_results = mmr(
            query_embedding=query_embedding,
            doc_embeddings=doc_embeddings,
            documents=mmr_candidates,
            top_k=self.final_k,
            lambda_param=0.6
        )

        return mmr_results
