from src.retriever.bm25_retriever import BM25Retriever
from src.retriever.query_engine import semantic_search
from src.utils.embedding_model import get_embedding_model
from src.retriever.mmr import mmr
import numpy as np


class HybridRetriever:
    def __init__(self, semantic_k=10, keyword_k=10, final_k=5):
        self.semantic_k = semantic_k
        self.keyword_k = keyword_k
        self.final_k = final_k
        self.bm25 = BM25Retriever()

    def search(self, query: str):
        semantic_results = semantic_search(query, top_k=self.semantic_k)
        for r in semantic_results:
            r["retrieval_type"] = "semantic"

        keyword_results = self.bm25.search(query, top_k=self.keyword_k)
        for r in keyword_results:
            r["retrieval_type"] = "keyword"

        merged = {}

        for r in semantic_results + keyword_results:
            key = r["id"]

            if key not in merged:
                merged[key] = r
                merged[key]["retrieval_types"] = {r["retrieval_type"]}
            else:
                merged[key]["retrieval_types"].add(r["retrieval_type"])

        for item in merged.values():
            item["retrieval_type"] = "+".join(sorted(item["retrieval_types"]))
            del item["retrieval_types"]

        return list(merged.values())

        
