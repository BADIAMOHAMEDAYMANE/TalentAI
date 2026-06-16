"""User request/response schemas."""
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class UserRegisterSchema:
    """Schema for user registration."""
    name: str
    email: str
    password: str
    role: str = "candidate"  # candidate | recruiter | admin

    def validate(self):
        """Validate user registration data."""
        if not self.name or len(self.name.strip()) == 0:
            raise ValueError("Name is required")
        if not self.email or "@" not in self.email:
            raise ValueError("Valid email is required")
        if not self.password or len(self.password) < 6:
            raise ValueError("Password must be at least 6 characters")
        if self.role not in ["candidate", "recruiter", "admin"]:
            raise ValueError("Invalid role. Must be candidate, recruiter, or admin")
        return True


@dataclass
class UserLoginSchema:
    """Schema for user login."""
    email: str
    password: str

    def validate(self):
        """Validate login data."""
        if not self.email or "@" not in self.email:
            raise ValueError("Valid email is required")
        if not self.password:
            raise ValueError("Password is required")
        return True


@dataclass
class UserResponseSchema:
    """Schema for user response."""
    id: int
    name: str
    email: str
    role: str
    created_at: str = ""

    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at,
        }
