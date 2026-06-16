# routes/cv.py
"""CV upload and candidate ranking endpoints."""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import CandidateService, RankingService
from app.utils import NotFoundError, ValidationError, BadRequestError, format_error_response

cv_bp = Blueprint("cv", __name__)


@cv_bp.post("/upload")
@jwt_required()
def upload_cv():
    """Upload and parse CV file."""
    try:
        user_id = get_jwt_identity()

        if "cv" not in request.files:
            return format_error_response("No file uploaded", 400)

        file = request.files["cv"]
        if not file.filename:
            return format_error_response("Empty filename", 400)

        # Save file
        path = f"/tmp/{file.filename}"
        file.save(path)

        # Process CV and store in database
        parsed = CandidateService.process_and_store_cv(int(user_id), path)

        return jsonify(parsed), 201

    except NotFoundError as e:
        return format_error_response(str(e), 404)
    except ValidationError as e:
        return format_error_response(str(e), 400)
    except Exception as e:
        return format_error_response(f"CV upload failed: {str(e)}", 500)


@cv_bp.post("/rank")
@jwt_required()
def rank_candidates():
    """Rank candidates by job description using specified algorithm."""
    try:
        data = request.get_json()

        if not data:
            return format_error_response("Request body is required", 400)

        job_description = data.get("job_description")
        method = data.get("method", "tfidf").lower()

        if not job_description:
            return format_error_response("'job_description' is required", 400)

        # Get all candidates with CV text
        candidates = CandidateService.get_all_candidates_for_ranking()

        if not candidates:
            return jsonify({
                "message": "No candidates found in database",
                "method_used": method,
                "total_candidates": 0,
                "ranking": []
            }), 200

        # Rank candidates
        ranked_list = RankingService.rank_candidates(job_description, candidates, method)

        # Remove sensitive cv_text from response
        for candidate in ranked_list:
            candidate.pop("text", None)

        return jsonify({
            "method_used": method,
            "total_candidates": len(ranked_list),
            "ranking": ranked_list
        }), 200

    except ValidationError as e:
        return format_error_response(str(e), 400)
    except BadRequestError as e:
        return format_error_response(str(e), 400)
    except Exception as e:
        return format_error_response(f"Ranking failed: {str(e)}", 500)
