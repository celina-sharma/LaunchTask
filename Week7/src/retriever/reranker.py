from sentence_transformers import CrossEncoder

class Reranker:
    def __init__(
        self,
        model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",
        top_k: int = 5
        ):
        self.model = CrossEncoder(model_name)
        self.top_k = top_k
        
        
    def rerank(self, query: str, candidates: list):
        print("[INFO] RERANKER EXECUTED")
        """
        candidates: list of dicts
        Each dict must contain at least:
        {
            "text": "...",
            "metadata": {...}
        }
        """
        if not candidates:
            return []
        
        #(query,chunks_text) pairs
        pairs = [(query, c["text"]) for c in candidates]
        
        #scored relevance
        scores = self.model.predict(pairs)
        
        #attach scores
        for c, score in zip(candidates,scores):
            c["rerank_score"] = float(score)
            
            
        #sort by  rerank score
        candidates = sorted(
            candidates,
            key=lambda x: x["rerank_score"],
            reverse=True
        )
        
        #return top-k reranked chunks
        return candidates[: self.top_k]