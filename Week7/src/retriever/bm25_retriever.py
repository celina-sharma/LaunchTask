import json
from pathlib import Path
from rank_bm25 import BM25Okapi

METADATA_PATH = Path("src/data/vectorstore/metadata.json")


class BM25Retriever:
    def __init__(self):
        self.documents = []
        self.tokenized_corpus = []

        self._load_documents()

        if not self.tokenized_corpus:
            raise ValueError("BM25 corpus is empty. Check metadata.json")

        self.bm25 = BM25Okapi(self.tokenized_corpus)

    def _load_documents(self):
        with open(METADATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        for item in data:
            text = item["text"]
            self.documents.append(item)
            self.tokenized_corpus.append(text.lower().split())

    def search(self, query: str, top_k: int = 5):
        query_tokens = query.lower().split()
        scores = self.bm25.get_scores(query_tokens)

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )[:top_k]

        results = []
        for idx in ranked_indices:
            doc = self.documents[idx]
            results.append({
                "id": doc["id"],
                "text": doc["text"],
                "metadata": doc["metadata"],
                "score": float(scores[idx]),
                "retrieval_type": "keyword"
            })

        return results
