import numpy as np

def compare_clip_embeddings(emb1, emb2):
    if len(emb1) == 0 or len(emb2) == 0:
        return 0.0

    norm1 = np.linalg.norm(emb1, axis=1, keepdims=True)
    norm2 = np.linalg.norm(emb2, axis=1, keepdims=True)
    similarity_matrix = np.dot(emb1, emb2.T) / (norm1 * norm2.T)

    best_for_emb1 = np.max(similarity_matrix, axis=1)
    best_for_emb2 = np.max(similarity_matrix, axis=0)

    sim_threshold = 0.94
    coverage1 = float(np.mean(best_for_emb1 >= sim_threshold))
    coverage2 = float(np.mean(best_for_emb2 >= sim_threshold))
    coverage = min(coverage1, coverage2)

    combined = np.concatenate([best_for_emb1, best_for_emb2])
    median_best = float(np.median(combined))

    if median_best < 0.85:
        return float(median_best * 0.6)

    return float(median_best * 0.6 + coverage * 0.4)