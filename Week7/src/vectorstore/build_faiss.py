import json
import faiss
import numpy as np
from pathlib import Path

# ---------- CONFIG ----------
EMBEDDINGS_JSON = Path("src/data/embeddings/embeddings.json")
EMBEDDINGS_NPY = Path("src/data/embeddings/embeddings.npy")

VECTORSTORE_DIR = Path("src/data/vectorstore")
INDEX_FILE = VECTORSTORE_DIR / "index.faiss"
METADATA_FILE = VECTORSTORE_DIR / "metadata.json"
# ----------------------------


def load_embeddings():
    """
    Load embeddings and metadata from embeddings.json
    """
    with open(EMBEDDINGS_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    vectors = []
    metadata = []

    for item in data:
        vectors.append(item["embedding"])

        # 🔥 CRITICAL FIX: store TEXT + SOURCE
        metadata.append({
            "text": item["text"],
            "source": item["metadata"]["source"]
        })

    vectors = np.array(vectors, dtype="float32")
    return vectors, metadata


def save_embeddings_npy(vectors):
    """
    Save raw embeddings as .npy file
    """
    EMBEDDINGS_NPY.parent.mkdir(parents=True, exist_ok=True)
    np.save(EMBEDDINGS_NPY, vectors)
    print(f"[✓] Embeddings saved at {EMBEDDINGS_NPY}")


def build_faiss_index(vectors):
    """
    Build FAISS index (cosine similarity via Inner Product)
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

    print(f"[✓] FAISS index saved at {INDEX_FILE}")
    print(f"[✓] Metadata saved at {METADATA_FILE}")


def main():
    print("[INFO] Loading embeddings from JSON...")
    vectors, metadata = load_embeddings()
    print(f"[INFO] Total vectors: {vectors.shape[0]}")

    save_embeddings_npy(vectors)

    print("[INFO] Building FAISS index...")
    index = build_faiss_index(vectors)

    save_faiss_index(index, metadata)


if __name__ == "__main__":
    main()
