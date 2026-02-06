import json
from pathlib import Path
from rank_bm25 import BM25Okapi


CHUNKS_DIR = Path("src/data/chunks")

class BM25Retriever:
    def __init__(self):
        self.texts = []
        self.metadatas = []

        self._load_chunks()
        self.tokenized_corpus = [text.lower().split() for text in self.texts]
        self.bm25 = BM25Okapi(self.tokenized_corpus)

    def _load_chunks(self):
        for file in CHUNKS_DIR.glob("*.json"):
            with open(file, "r", encoding="utf-8") as f:
                chunks = json.load(f)
                for c in chunks:
                    self.texts.append(c["text"])
                    self.metadatas.append(c["metadata"])

    def search(self, query: str, top_k: int = 5):
        query_tokens = query.lower().split()
        scores = self.bm25.get_scores(query_tokens)

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )[:top_k]

        results = []
        for i in ranked_indices:
            results.append({
                "text": self.texts[i],
                "metadata": self.metadatas[i],
                "score": float(scores[i]),
                "source": "bm25"
            })

        return results
