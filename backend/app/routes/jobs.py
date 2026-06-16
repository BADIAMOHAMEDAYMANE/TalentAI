"""Job management endpoints."""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import JobService
from app.utils import NotFoundError, ValidationError, recruiter_or_admin, format_error_response, get_current_user

jobs_bp = Blueprint("jobs", __name__)


@jobs_bp.post("")
@recruiter_or_admin
def create_job():
    """Create a new job posting."""
    try:
        user = get_current_user()
        data = request.get_json()

        if not data:
            return format_error_response("Request body is required", 400)

        job = JobService.create_job(user.id, data)
        return jsonify({"message": "Job created successfully", "job": job}), 201

    except ValidationError as e:
        return format_error_response(str(e), 400)
    except NotFoundError as e:
        return format_error_response(str(e), 404)
    except Exception as e:
        return format_error_response(f"Job creation failed: {str(e)}", 500)


@jobs_bp.get("/<int:job_id>")
def get_job(job_id):
    """Get job by ID."""
    try:
        job = JobService.get_job(job_id)
        return jsonify(job), 200

    except NotFoundError as e:
        return format_error_response(str(e), 404)
    except Exception as e:
        return format_error_response(f"Failed to fetch job: {str(e)}", 500)


@jobs_bp.get("")
def list_jobs():
    """List all jobs with pagination."""
    try:
        limit = request.args.get("limit", 50, type=int)
        offset = request.args.get("offset", 0, type=int)

        jobs = JobService.list_jobs(limit, offset)
        return jsonify({"total": len(jobs), "jobs": jobs}), 200

    except Exception as e:
        return format_error_response(f"Failed to fetch jobs: {str(e)}", 500)


@jobs_bp.delete("/<int:job_id>")
@recruiter_or_admin
def delete_job(job_id):
    """Delete a job posting."""
    try:
        user = get_current_user()
        JobService.delete_job(job_id, user.id)
        return jsonify({"message": "Job deleted successfully"}), 200

    except NotFoundError as e:
        return format_error_response(str(e), 404)
    except ValidationError as e:
        return format_error_response(str(e), 403)
    except Exception as e:
        return format_error_response(f"Job deletion failed: {str(e)}", 500)
