"""Candidate profile and ranking request schemas."""
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class CandidateProfileSchema:
    """Schema for candidate profile response."""
    user_id: int
    skills: Optional[List[str]] = None
    experience: Optional[int] = None
    education: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    updated_at: str = ""

    def to_dict(self):
        """Convert to dictionary."""
        return {
            "user_id": self.user_id,
            "skills": self.skills,
            "experience": self.experience,
            "education": self.education,
            "phone": self.phone,
            "linkedin": self.linkedin,
            "updated_at": self.updated_at,
        }


@dataclass
class RankingRequestSchema:
    """Schema for candidate ranking request."""
    job_description: str
    method: str = "tfidf"  # tfidf | semantic

    def validate(self):
        """Validate ranking request."""
        if not self.job_description or len(self.job_description.strip()) == 0:
            raise ValueError("Job description is required")
        if self.method not in ["tfidf", "semantic"]:
            raise ValueError("Method must be 'tfidf' or 'semantic'")
        return True


@dataclass
class CandidateRankResponseSchema:
    """Schema for ranked candidate response."""
    user_id: int
    skills: Optional[List[str]] = None
    experience: Optional[int] = None
    education: Optional[str] = None
    score: float = 0.0

    def to_dict(self):
        """Convert to dictionary."""
        return {
            "user_id": self.user_id,
            "skills": self.skills,
            "experience": self.experience,
            "education": self.education,
            "score": self.score,
        }
