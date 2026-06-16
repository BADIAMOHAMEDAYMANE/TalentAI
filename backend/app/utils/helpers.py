"""Helper functions for TalentAI."""
from functools import wraps
from flask import current_app, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import get_jwt_identity
from app.models import User
from app.utils.errors import AuthorizationError, NotFoundError


def hash_password(password: str) -> str:
    """Hash password using werkzeug."""
    return generate_password_hash(password)


def verify_password(hashed_password: str, password: str) -> bool:
    """Verify password against hash."""
    return check_password_hash(hashed_password, password)


def get_current_user() -> User:
    """Get current authenticated user from JWT token."""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        raise NotFoundError(f"User with id {user_id} not found")
    return user


def format_error_response(message: str, status_code: int = 400):
    """Format error response."""
    return jsonify({"error": message}), status_code


def format_success_response(data, status_code: int = 200):
    """Format success response."""
    return jsonify(data), status_code
