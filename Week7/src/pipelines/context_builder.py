def build_context_json(chunks, query, max_chars=6000):
    context_items = []
    current_len = 0

    for i, chunk in enumerate(chunks, 1):
        text = chunk["text"].strip()

        # limit per chunk for readability
        PREVIEW_CHARS = 800
        if len(text) > PREVIEW_CHARS:
            text = text[:PREVIEW_CHARS] + "..."

        item = {
            "id": i,
            "source": chunk["metadata"]["source"],
            "retrieval_type": chunk.get("retrieval_type", "unknown"),
            "text": text
        }

        if current_len + len(text) > max_chars:
            break

        context_items.append(item)
        current_len += len(text)

    return {
        "query": query,
        "contexts": context_items
    }
