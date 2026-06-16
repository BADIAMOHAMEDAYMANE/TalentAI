"""Job request/response schemas."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class JobCreateSchema:
    """Schema for job creation."""
    title: str
    description: str
    location: Optional[str] = None
    salary: Optional[str] = None
    experience: int = 0

    def validate(self):
        """Validate job data."""
        if not self.title or len(self.title.strip()) == 0:
            raise ValueError("Job title is required")
        if not self.description or len(self.description.strip()) == 0:
            raise ValueError("Job description is required")
        if self.experience < 0:
            raise ValueError("Experience cannot be negative")
        return True


@dataclass
class JobResponseSchema:
    """Schema for job response."""
    id: int
    title: str
    description: str
    location: Optional[str] = None
    salary: Optional[str] = None
    experience: int = 0
    recruiter_id: Optional[int] = None
    created_at: str = ""

    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "location": self.location,
            "salary": self.salary,
            "experience": self.experience,
            "recruiter_id": self.recruiter_id,
            "created_at": self.created_at,
        }
