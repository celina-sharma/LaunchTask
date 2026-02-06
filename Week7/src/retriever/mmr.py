import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def mmr(
    query_embedding,
    doc_embeddings,
    documents,
    top_k=5,
    lambda_param=0.6
):
    """
    Max Marginal Relevance (MMR)
    """
    selected = []
    selected_indices = []

    similarity_to_query = cosine_similarity(
        doc_embeddings, query_embedding.reshape(1, -1)
    ).flatten()

    while len(selected) < min(top_k, len(documents)):
        if len(selected) == 0:
            idx = int(np.argmax(similarity_to_query))
            selected.append(documents[idx])
            selected_indices.append(idx)
            continue

        diversity = cosine_similarity(
            doc_embeddings,
            doc_embeddings[selected_indices]
        ).max(axis=1)

        mmr_scores = (
            lambda_param * similarity_to_query
            - (1 - lambda_param) * diversity
        )

        # exclude already selected docs
        for i in selected_indices:
            mmr_scores[i] = -np.inf

        idx = int(np.argmax(mmr_scores))
        selected.append(documents[idx])
        selected_indices.append(idx)

    return selected
