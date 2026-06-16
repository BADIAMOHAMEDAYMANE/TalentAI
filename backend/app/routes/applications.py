"""Job application endpoints."""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import ApplicationService
from app.utils import NotFoundError, ValidationError, recruiter_or_admin, candidate_or_admin, format_error_response, get_current_user

applications_bp = Blueprint("applications", __name__)


@applications_bp.post("")
@candidate_or_admin
def create_application():
    """Create a job application."""
    try:
        data = request.get_json()

        if not data:
            return format_error_response("Request body is required", 400)

        application = ApplicationService.create_application(data)
        return jsonify({"message": "Application created successfully", "application": application}), 201

    except ValidationError as e:
        return format_error_response(str(e), 400)
    except NotFoundError as e:
        return format_error_response(str(e), 404)
    except Exception as e:
        return format_error_response(f"Application creation failed: {str(e)}", 500)


@applications_bp.get("/<int:application_id>")
def get_application(application_id):
    """Get application by ID."""
    try:
        application = ApplicationService.get_application(application_id)
        return jsonify(application), 200

    except NotFoundError as e:
        return format_error_response(str(e), 404)
    except Exception as e:
        return format_error_response(f"Failed to fetch application: {str(e)}", 500)


@applications_bp.patch("/<int:application_id>")
@recruiter_or_admin
def update_application_status(application_id):
    """Update application status."""
    try:
        data = request.get_json()

        if not data:
            return format_error_response("Request body is required", 400)

        application = ApplicationService.update_application_status(application_id, data)
        return jsonify({"message": "Application updated successfully", "application": application}), 200

    except ValidationError as e:
        return format_error_response(str(e), 400)
    except NotFoundError as e:
        return format_error_response(str(e), 404)
    except Exception as e:
        return format_error_response(f"Application update failed: {str(e)}", 500)


@applications_bp.get("/job/<int:job_id>")
def get_job_applications(job_id):
    """Get all applications for a job."""
    try:
        applications = ApplicationService.list_applications_for_job(job_id)
        return jsonify({"total": len(applications), "applications": applications}), 200

    except Exception as e:
        return format_error_response(f"Failed to fetch applications: {str(e)}", 500)


@applications_bp.get("/candidate/<int:candidate_id>")
def get_candidate_applications(candidate_id):
    """Get all applications from a candidate."""
    try:
        applications = ApplicationService.list_applications_for_candidate(candidate_id)
        return jsonify({"total": len(applications), "applications": applications}), 200

    except Exception as e:
        return format_error_response(f"Failed to fetch applications: {str(e)}", 500)
