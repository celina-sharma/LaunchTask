import json
import faiss
import numpy as np
from pathlib import Path


EMBEDDINGS_JSONL = Path("src/data/embeddings/embeddings.jsonl")

VECTORSTORE_DIR = Path("src/data/vectorstore")
INDEX_FILE = VECTORSTORE_DIR / "index.faiss"
METADATA_FILE = VECTORSTORE_DIR / "metadata.json"


def load_embeddings():
    """
    Load embeddings and metadata from embeddings.jsonl (JSONL format)
    """
    vectors = []
    metadata = []

    with open(EMBEDDINGS_JSONL, "r", encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)

            vectors.append(record["vector"])
            metadata.append({
                "id": record["id"],
                "text": record["text"],
                "metadata": record["metadata"],
            })

    vectors = np.array(vectors, dtype="float32")
    return vectors, metadata


def build_faiss_index(vectors):
    """
    Build FAISS index using Inner Product (cosine similarity).
    Assumes embeddings are already normalized.
    """
    dim = vectors.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(vectors)
    return index


def save_faiss_index(index, metadata):
    """
    Save FAISS index and metadata
    """
    VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)

    faiss.write_index(index, str(INDEX_FILE))

    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print(f"FAISS index saved → {INDEX_FILE}")
    print(f"Metadata saved → {METADATA_FILE}")


def main():
    print("[INFO] Loading embeddings...")
    vectors, metadata = load_embeddings()

    if len(vectors) == 0:
        print("[ERROR] No embeddings found. Exiting.")
        return

    print(f"[INFO] Total vectors loaded: {vectors.shape[0]}")

    print("[INFO] Building FAISS index...")
    index = build_faiss_index(vectors)

    save_faiss_index(index, metadata)


if __name__ == "__main__":
    main()
