from sentence_transformers import SentenceTransformer

_MODEL = None

def get_embedding_model():
    global _MODEL
    if _MODEL is None:
        _MODEL = SentenceTransformer("BAAI/bge-small-en")
    return _MODEL
