import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
import numpy as np

# -------- CONFIG --------
CHUNKS_DIR = Path("src/data/chunks")
EMBEDDINGS_DIR = Path("src/data/embeddings")
MODEL_NAME = "BAAI/bge-small-en"
# ------------------------


def load_chunks():
    all_chunks = []
    for file in CHUNKS_DIR.glob("chunks_*.json"):
        with open(file, "r", encoding="utf-8") as f:
            chunks = json.load(f)
            all_chunks.extend(chunks)
    return all_chunks


def generate_embeddings(chunks, model):
    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts, show_progress_bar=True, normalize_embeddings = True)
    return embeddings


def save_embeddings(chunks, embeddings):
    EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)

    output = []
    for chunk, emb in zip(chunks, embeddings):
        output.append({
            "text": chunk["text"],
            "embedding": emb.tolist(),
            "metadata": chunk["metadata"]
        })

    out_path = EMBEDDINGS_DIR / "embeddings.json"
    outp = EMBEDDINGS_DIR / "embeddings.npy"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f)
    
    np.save(outp , embeddings)

    print(f"[✓] Saved {len(output)} embeddings to {out_path}")


def main():
    print("[INFO] Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)

    print("[INFO] Loading chunks...")
    chunks = load_chunks()
    print(f"[INFO] Total chunks: {len(chunks)}")

    print("[INFO] Generating embeddings...")
    embeddings = generate_embeddings(chunks, model)

    save_embeddings(chunks, embeddings)


if __name__ == "__main__":
    main()
