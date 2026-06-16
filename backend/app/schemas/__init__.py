"""Schemas for request/response validation."""
from app.schemas.user_schema import UserRegisterSchema, UserLoginSchema, UserResponseSchema
from app.schemas.job_schema import JobCreateSchema, JobResponseSchema
from app.schemas.candidate_schema import (
    CandidateProfileSchema,
    RankingRequestSchema,
    CandidateRankResponseSchema,
)
from app.schemas.application_schema import (
    ApplicationCreateSchema,
    ApplicationUpdateSchema,
    ApplicationResponseSchema,
)

__all__ = [
    "UserRegisterSchema",
    "UserLoginSchema",
    "UserResponseSchema",
    "JobCreateSchema",
    "JobResponseSchema",
    "CandidateProfileSchema",
    "RankingRequestSchema",
    "CandidateRankResponseSchema",
    "ApplicationCreateSchema",
    "ApplicationUpdateSchema",
    "ApplicationResponseSchema",
]
