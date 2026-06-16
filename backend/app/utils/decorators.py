"""Custom decorators for TalentAI."""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required as jwt_required_decorator
from app.utils.helpers import get_current_user
from app.utils.errors import AuthorizationError


def role_required(*allowed_roles):
    """Decorator to enforce role-based access control.

    Usage:
        @role_required("recruiter", "admin")
        def create_job():
            ...
    """
    def decorator(fn):
        @wraps(fn)
        @jwt_required_decorator()
        def wrapper(*args, **kwargs):
            user = get_current_user()
            if user.role not in allowed_roles:
                return jsonify({
                    "error": f"Access denied. Required roles: {', '.join(allowed_roles)}"
                }), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def candidate_or_admin(fn):
    """Decorator to allow only candidates and admins."""
    @wraps(fn)
    @jwt_required_decorator()
    def wrapper(*args, **kwargs):
        user = get_current_user()
        if user.role not in ["candidate", "admin"]:
            return jsonify({"error": "Access denied. Candidates and admins only."}), 403
        return fn(*args, **kwargs)
    return wrapper


def recruiter_or_admin(fn):
    """Decorator to allow only recruiters and admins."""
    @wraps(fn)
    @jwt_required_decorator()
    def wrapper(*args, **kwargs):
        user = get_current_user()
        if user.role not in ["recruiter", "admin"]:
            return jsonify({"error": "Access denied. Recruiters and admins only."}), 403
        return fn(*args, **kwargs)
    return wrapper
