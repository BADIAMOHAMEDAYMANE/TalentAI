# ranking/semantic.py
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

def rank_candidates_semantic(job_description: str, candidates: list[dict]) -> list[dict]:
    """
    Trie les candidats basé sur la similarité contextuelle et sémantique.
    """
    if not candidates:
        return []

    job_emb = model.encode(job_description, convert_to_tensor=True)
    cand_embs = model.encode([c["text"] for c in candidates], convert_to_tensor=True)
    scores = util.cos_sim(job_emb, cand_embs)[0]

    ranked_candidates = []
    for i, c in enumerate(candidates):
        candidate_copy = c.copy()
        candidate_copy["score"] = round(float(scores[i]) * 100, 1)
        ranked_candidates.append(candidate_copy)

    return sorted(ranked_candidates, key=lambda x: x["score"], reverse=True)