from sentence_transformers import SentenceTransformer

_MODEL = None

def get_embedding_model():
    global _MODEL

    if _MODEL is None:
        print("[INFO] Loading embedding model (singleton)...")
        _MODEL = SentenceTransformer("BAAI/bge-base-en-v1.5")
    return _MODEL
