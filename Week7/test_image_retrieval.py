from retriever.image_retriever import ImageRetriever

query = "Comparison of cumulative total return"

retriever = ImageRetriever()
results = retriever.search(query, top_k=5)

print("\nIMAGE RETRIEVAL RESULTS\n")

for i, r in enumerate(results, 1):
    print(f"{i}. Source: {r['source_pdf']} | Page: {r['page']}")
    print(f"   Score: {r['score']:.4f}")
    print(f"   Caption: {r['caption']}")
    print("-" * 60)
