"""Application request/response schemas."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class ApplicationCreateSchema:
    """Schema for application creation."""
    candidate_id: int
    job_id: int
    score: Optional[float] = None

    def validate(self):
        """Validate application data."""
        if self.candidate_id <= 0:
            raise ValueError("Valid candidate_id is required")
        if self.job_id <= 0:
            raise ValueError("Valid job_id is required")
        if self.score is not None and (self.score < 0 or self.score > 100):
            raise ValueError("Score must be between 0 and 100")
        return True


@dataclass
class ApplicationUpdateSchema:
    """Schema for application status update."""
    status: str  # applied | under_review | interview | accepted | rejected

    def validate(self):
        """Validate application update."""
        valid_statuses = ["applied", "under_review", "interview", "accepted", "rejected"]
        if self.status not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return True


@dataclass
class ApplicationResponseSchema:
    """Schema for application response."""
    id: int
    candidate_id: int
    job_id: int
    status: str
    score: Optional[float] = None
    applied_at: str = ""

    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": self.id,
            "candidate_id": self.candidate_id,
            "job_id": self.job_id,
            "status": self.status,
            "score": self.score,
            "applied_at": self.applied_at,
        }
