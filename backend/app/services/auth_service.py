"""Authentication and user management service."""
from flask_jwt_extended import create_access_token
from app import db
from app.models import User
from app.schemas import UserRegisterSchema, UserLoginSchema
from app.utils import hash_password, verify_password, ConflictError, AuthenticationError, ValidationError


class AuthService:
    """Service for authentication and user management."""

    @staticmethod
    def register_user(data: dict) -> dict:
        """Register a new user.

        Args:
            data: Dictionary with name, email, password, role

        Returns:
            Dictionary with user details

        Raises:
            ValidationError: If data is invalid
            ConflictError: If email already exists
        """
        schema = UserRegisterSchema(**data)
        schema.validate()

        # Check if email exists
        existing_user = User.query.filter_by(email=schema.email).first()
        if existing_user:
            raise ConflictError(f"Email {schema.email} is already registered")

        # Create user
        user = User(
            name=schema.name,
            email=schema.email,
            password=hash_password(schema.password),
            role=schema.role,
        )
        db.session.add(user)
        db.session.commit()

        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at.isoformat(),
        }

    @staticmethod
    def authenticate_user(email: str, password: str) -> dict:
        """Authenticate user and return JWT token.

        Args:
            email: User email
            password: User password

        Returns:
            Dictionary with access_token and user details

        Raises:
            AuthenticationError: If credentials are invalid
        """
        schema = UserLoginSchema(email=email, password=password)
        schema.validate()

        user = User.query.filter_by(email=schema.email).first()

        if not user or not verify_password(user.password, schema.password):
            raise AuthenticationError("Invalid email or password")

        access_token = create_access_token(identity=str(user.id))

        return {
            "access_token": access_token,
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
            },
        }
