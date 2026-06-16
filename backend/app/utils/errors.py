"""Custom exceptions for TalentAI application."""


class TalentAIError(Exception):
    """Base exception for TalentAI."""
    pass


class ValidationError(TalentAIError):
    """Raised when validation fails."""
    pass


class AuthenticationError(TalentAIError):
    """Raised when authentication fails."""
    pass


class AuthorizationError(TalentAIError):
    """Raised when user is not authorized."""
    pass


class NotFoundError(TalentAIError):
    """Raised when resource is not found."""
    pass


class ConflictError(TalentAIError):
    """Raised when resource already exists."""
    pass


class BadRequestError(TalentAIError):
    """Raised for bad request."""
    pass
