def hybrid_rerank(vector_results, graph_results):
    scores = {}

    for text in vector_results:
        scores[text] = scores.get(text, 0) + 2.0  # semantic weight

    for text in graph_results:
        scores[text] = scores.get(text, 0) + 1.0  # graph relevance

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [text for text, _ in ranked][:5]
