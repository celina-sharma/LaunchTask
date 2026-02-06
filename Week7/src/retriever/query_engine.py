import json
import faiss
import numpy as np
from pathlib import Path
from src.utils.embedding_model import get_embedding_model

INDEX_PATH = Path("src/data/vectorstore/index.faiss")
META_PATH = Path("src/data/vectorstore/metadata.json")
EMBEDDINGS_NPY = Path("src/data/embeddings/embeddings.npy")


def load_index():
    """
    Load FAISS index, metadata, and stored document embeddings
    """
    index = faiss.read_index(str(INDEX_PATH))

    with open(META_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    embeddings = np.load(EMBEDDINGS_NPY).astype("float32")

    return index, metadata, embeddings


def semantic_search(query: str, top_k: int = 5):
    """
    FAISS-based semantic search (cosine similarity).
    """
    model = get_embedding_model()
    index, metadata, embeddings = load_index()

    query_embedding = model.encode(
        query,
        normalize_embeddings=True
    ).astype("float32")

    scores, indices = index.search(
        query_embedding.reshape(1, -1),
        top_k
    )

    results = []
    for idx, score in zip(indices[0], scores[0]):
        results.append({
            "id": metadata[idx]["id"],
            "text": metadata[idx]["text"],
            "metadata": {
                "source": metadata[idx]["metadata"]["source"],
                "page": metadata[idx]["metadata"].get("page")
            },
            "score": float(score),
            # used later for MMR
            "embedding": embeddings[idx]
        })

    return results

if __name__ == "__main__":
    query = input("Enter your question: ")
    results = semantic_search(query)

    print("\nRetrieved Context:\n")
    for i, r in enumerate(results, 1):
        print(f"--- Result {i} ---")
        print(f"Source: {r['metadata']['source']}")
        print(f"Score: {r['score']:.4f}")
        print(r["text"][:300])
        print("-" * 60)
