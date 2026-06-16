# app/routes/auth.py
"""Authentication endpoints."""
from flask import Blueprint, request, jsonify
from app.services import AuthService
from app.utils import ValidationError, AuthenticationError, ConflictError, format_error_response

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
def register():
    """Register a new user."""
    try:
        data = request.get_json()
        if not data:
            return format_error_response("Request body is required", 400)

        user = AuthService.register_user(data)
        return jsonify({
            "message": "User created successfully",
            "user": user
        }), 201

    except ValidationError as e:
        return format_error_response(str(e), 400)
    except ConflictError as e:
        return format_error_response(str(e), 409)
    except Exception as e:
        return format_error_response(f"Registration failed: {str(e)}", 500)


@auth_bp.post("/login")
def login():
    """Authenticate user and return JWT token."""
    try:
        data = request.get_json()
        if not data:
            return format_error_response("Request body is required", 400)

        result = AuthService.authenticate_user(
            email=data.get("email"),
            password=data.get("password")
        )
        return jsonify(result), 200

    except ValidationError as e:
        return format_error_response(str(e), 400)
    except AuthenticationError as e:
        return format_error_response(str(e), 401)
    except Exception as e:
        return format_error_response(f"Login failed: {str(e)}", 500)
