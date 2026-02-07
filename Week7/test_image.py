from retriever.image_retriever import ImageRetriever

QUERY_IMAGE = "src/data/images/report5/page_49_img_1.png"

retriever = ImageRetriever()
results = retriever.search_by_image(QUERY_IMAGE, top_k=5)

print("\nIMAGE → IMAGE RETRIEVAL RESULTS\n")

for i, r in enumerate(results, 1):
    print(f"{i}. Source: {r['source_pdf']} | Page: {r['page']}")
    print(f"   Score: {r['score']:.4f}")
    print(f"   Caption: {r['caption']}")
    print("-" * 60)
