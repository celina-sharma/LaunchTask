def build_context_json(chunks, query, max_chars=6000):
    context_items = []
    current_len = 0
    PREVIEW_CHARS = 800

    for i, chunk in enumerate(chunks, 1):
        text = chunk.get("text", "").strip()

        if not text:
            continue

        if len(text) > PREVIEW_CHARS:
            text = text[:PREVIEW_CHARS] + "..."

        if current_len + len(text) > max_chars:
            break

        item = {
            "id": i,
            "source": chunk.get("metadata", {}).get("source", "unknown"),
            "retrieval_type": chunk.get("retrieval_type", "unknown"),
            "text": text
        }

        context_items.append(item)
        current_len += len(text)

    return {
        "query": query,
        "contexts": context_items
    }


    