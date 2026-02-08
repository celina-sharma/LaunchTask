import json
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image

IMAGE_DATA = Path("src/data/images/image_metadata_with_embeddings.json")
MODEL_NAME = "clip-ViT-B-32"

class ImageRetriever:
    def __init__(self):
        print("[INFO] Loading CLIP model for image retrieval...")
        self.model = SentenceTransformer(MODEL_NAME)

        with open(IMAGE_DATA, "r", encoding="utf-8") as f:
            self.data = json.load(f)

        self.image_embeddings = np.array(
            [d["image_embedding"] for d in self.data],
            dtype="float32"
        )

    def search(self, query: str, top_k: int = 5):
        #enco
        query_embedding = self.model.encode(
            query,
            normalize_embeddings=True
        ).reshape(1, -1)
        
        scores = cosine_similarity(
            query_embedding,
            self.image_embeddings
        )[0]

        top_indices = scores.argsort()[::-1][:top_k]

        results = []                     
        for idx in top_indices:
            item = self.data[idx]
            results.append({
                "image_id": item["image_id"],
                "image_path": item["image_path"],
                "source_pdf": item["source_pdf"],
                "page": item["page"],
                "caption": item.get("caption", ""),
                "ocr_text": item.get("ocr_text", ""),
                "score": float(scores[idx])
        })


        return results
    
    def search_by_image(self, image_path: str, top_k: int = 5):
        """
        Image → Image search using CLIP image embeddings
        """
        
        query_embedding = self.model.encode(
            Image.open(image_path).convert("RGB"),
            normalize_embeddings=True
        ).reshape(1, -1)

        scores = cosine_similarity(
            query_embedding,
            self.image_embeddings
        )[0]

        top_indices = scores.argsort()[::-1][:top_k]

        results = []
        for idx in top_indices:
            item = self.data[idx]
            results.append({
                "image_id": item["image_id"],
                "image_path": item["image_path"],
                "source_pdf": item["source_pdf"],
                "page": item["page"],
                "caption": item.get("caption", ""),
                "ocr_text": item.get("ocr_text", ""),
                "score": float(scores[idx])
            })

        return results

