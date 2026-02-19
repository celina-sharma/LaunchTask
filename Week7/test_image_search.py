from src.retriever.image_retriever import ImageRetriever

if __name__ == "__main__":
    r = ImageRetriever()
    results = r.search("Comparison of cumulative return", top_k=5)

    for i, res in enumerate(results, 1):
        print(f"\nResult {i}")
        print(f"Image ID: {res['image_id']}")
        print(f"Score: {res['score']}")
        print(f"Caption: {res['caption']}")
        print(f"OCR: {res['ocr_text']}")
