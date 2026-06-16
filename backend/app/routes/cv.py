# routes/cv.py
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import CandidateProfile
from app import db
from app.services.parser.nlp import parse_cv
from app.services.parser.extractor import extract_text

from app.services.ranking.tfidf import rank_candidates_tfidf
from app.services.ranking.semantic import rank_candidates_semantic

cv_bp = Blueprint("cv", __name__)  

@cv_bp.post("/upload")
@jwt_required()
def upload_cv():
    user_id = get_jwt_identity()
    if "cv" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
        
    file    = request.files["cv"]
    path    = f"/tmp/{file.filename}"
    file.save(path)

    text   = extract_text(path)
    parsed = parse_cv(text)

    profile = CandidateProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        profile = CandidateProfile(user_id=user_id)
        db.session.add(profile)

    profile.skills     = parsed["skills"]
    profile.experience = parsed["experience"]
    profile.education  = parsed["education"]
    profile.cv_text    = text
    profile.cv_path    = path
    db.session.commit()

    return jsonify(parsed), 201


@cv_bp.post("/rank")
@jwt_required()
def rank_candidates():
    """
    Endpoint pour classer les candidats par rapport à une description de poste (Job Description).
    Prend en entrée un JSON contenant la 'job_description' et la 'method' souhaitée ('tfidf' ou 'semantic').
    """
    data = request.get_json()
    
    if not data or "job_description" not in data:
        return jsonify({"error": "Missing 'job_description' in request body"}), 400
        
    job_description = data["job_description"]
    method = data.get("method", "tfidf").lower()

    profiles = CandidateProfile.query.all()
    if not profiles:
        return jsonify({"message": "No candidates found in database", "candidates": []}), 200

    candidates_list = [
        {
            "user_id": p.user_id,
            "skills": p.skills,
            "experience": p.experience,
            "education": p.education,
            "text": p.cv_text  
        }
        for p in profiles if p.cv_text 
    ]

    if method == "semantic":
        ranked_list = rank_candidates_semantic(job_description, candidates_list)
        
    elif method == "tfidf":
        ranked_list = rank_candidates_tfidf(job_description, candidates_list)
    else:
        return jsonify({"error": f"Unknown ranking method '{method}'. Use 'tfidf' or 'semantic'."}), 400

    # Sécurité au cas où l'algorithme de ranking retournerait None
    if not ranked_list:
        ranked_list = []

    for candidate in ranked_list:
        candidate.pop("text", None)

    return jsonify({
        "method_used": method,
        "total_candidates": len(ranked_list),
        "ranking": ranked_list
    }), 200