# ranking/tfidf.py 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def rank_candidates_tfidf(job_description: str, candidates: list[dict]) -> list[dict]:
    """
    Trie les candidats basé sur la fréquence et la rareté des mots-clés (exact match).
    """
    if not candidates:
        return []

    corpus = [job_description] + [c["text"] for c in candidates]
    
    # "english" par défaut, à adapter ou retirer si tes CVs sont en français
    tfidf = TfidfVectorizer(stop_words="english") 
    matrix = tfidf.fit_transform(corpus)

    job_vec = matrix[0]
    cand_vecs = matrix[1:]
    scores = cosine_similarity(job_vec, cand_vecs).flatten()

    ranked_candidates = []
    for i, c in enumerate(candidates):
        candidate_copy = c.copy()
        candidate_copy["score"] = round(float(scores[i]) * 100, 1)
        ranked_candidates.append(candidate_copy)

    return sorted(ranked_candidates, key=lambda x: x["score"], reverse=True)