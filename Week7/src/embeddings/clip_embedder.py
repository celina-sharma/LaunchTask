import json
from pathlib import Path
from PIL import Image
import numpy as np
from sentence_transformers import SentenceTransformer

IMAGE_METADATA = Path("src/data/images/image_metadata.json")
OUTPUT_METADATA = Path("src/data/images/image_metadata_with_embeddings.json")


class CLIPEmbedder:
    def __init__(self):
        print("[INFO] Loading CLIP model (SentenceTransformers)...")
        self.model = SentenceTransformer("clip-ViT-B-32")

    def embed_image(self, image_path: str):
        image = Image.open(image_path).convert("RGB")
        embedding = self.model.encode(
            image,
            normalize_embeddings=True
        )
        return embedding

    def embed_text(self, text: str):
        embedding = self.model.encode(
            text,
            normalize_embeddings=True
        )
        return embedding


def main():
    print("[INFO] Loading image metadata...")
    with open(IMAGE_METADATA, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    embedder = CLIPEmbedder()

    print("[INFO] Generating CLIP embeddings...")
    for item in metadata:
        try:
            item["image_embedding"] = embedder.embed_image(
                item["image_path"]
            ).tolist()
            
            combined_text = f"{item.get('caption','')} {item.get('ocr_text','')}".strip()
            item["text_embedding"] = embedder.embed_text(
                combined_text if combined_text else " "
            ).tolist()

        except Exception as e:
            print(f"[WARN] Embedding failed for {item['image_id']}: {e}")
            item["image_embedding"] = []
            item["text_embedding"] = []

    with open(OUTPUT_METADATA, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print("CLIP embeddings generated successfully")
    print(f"Saved to {OUTPUT_METADATA}")


if __name__ == "__main__":
    main()
