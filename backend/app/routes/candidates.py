"""Candidate profile endpoints."""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import CandidateService
from app.utils import NotFoundError, candidate_or_admin, format_error_response, get_current_user

candidates_bp = Blueprint("candidates", __name__)


@candidates_bp.get("/me")
@candidate_or_admin
def get_my_profile():
    """Get current user's candidate profile."""
    try:
        user = get_current_user()
        profile = CandidateService.get_candidate_profile(user.id)
        return jsonify(profile), 200

    except NotFoundError as e:
        return format_error_response(str(e), 404)
    except Exception as e:
        return format_error_response(f"Failed to fetch profile: {str(e)}", 500)


@candidates_bp.get("/<int:user_id>")
def get_candidate_profile(user_id):
    """Get candidate profile by user ID."""
    try:
        profile = CandidateService.get_candidate_profile(user_id)
        return jsonify(profile), 200

    except NotFoundError as e:
        return format_error_response(str(e), 404)
    except Exception as e:
        return format_error_response(f"Failed to fetch profile: {str(e)}", 500)
