import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

CHUNKS_DIR = Path("src/data/chunks")
EMBEDDINGS_DIR = Path("src/data/embeddings")

MODEL_NAME = "BAAI/bge-base-en-v1.5"
BATCH_SIZE = 32

OUTPUT_JSON = EMBEDDINGS_DIR / "embeddings.jsonl"
OUTPUT_NPY = EMBEDDINGS_DIR / "embeddings.npy"



def load_chunks():
    """
    Loads chunks from JSONL files.
    Each line = one JSON object.
    """
    all_chunks = []

    for file in sorted(CHUNKS_DIR.glob("*.jsonl")):
        print(f"[INFO] Loading chunks from {file.name}")
        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                all_chunks.append(json.loads(line))

    return all_chunks


def generate_embeddings(chunks, model):
    """
    Generates embeddings in safe batches.
    """
    texts = [c["text"] for c in chunks]

    embeddings = model.encode(
        texts,
        batch_size=BATCH_SIZE,
        show_progress_bar=True,
        normalize_embeddings=True,
    )

    return embeddings


def save_embeddings(chunks, embeddings):
    """
    Saves embeddings in:
    - JSONL (text + metadata + vector)
    - NPY (pure vectors for fast loading)
    """
    EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        for chunk, emb in zip(chunks, embeddings):
            record = {
                "id": chunk["chunk_id"],
                "text": chunk["text"],
                "vector": emb.tolist(),
                "metadata": chunk["metadata"],
            }
            f.write(json.dumps(record) + "\n")

    np.save(OUTPUT_NPY, embeddings)

    print(f"Saved {len(chunks)} embeddings")
    print(f"JSONL {OUTPUT_JSON}")
    print(f"NPY {OUTPUT_NPY}")


def main():
    print("[INFO] Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)

    print("[INFO] Loading chunks...")
    chunks = load_chunks()

    if not chunks:
        print("No chunks found. Exiting.")
        return

    print(f"[INFO] Total chunks loaded: {len(chunks)}")

    print("[INFO] Generating embeddings...")
    embeddings = generate_embeddings(chunks, model)

    save_embeddings(chunks, embeddings)


if __name__ == "__main__":
    main()
