"""Candidate profile management service."""
from app import db
from app.models import User, CandidateProfile
from app.utils import NotFoundError
from app.services.parser.extractor import extract_text
from app.services.parser.nlp import parse_cv


class CandidateService:
    """Service for candidate profile management."""

    @staticmethod
    def get_candidate_profile(user_id: int) -> dict:
        """Get candidate profile by user ID.

        Args:
            user_id: User ID

        Returns:
            Dictionary with candidate profile data

        Raises:
            NotFoundError: If candidate not found
        """
        profile = CandidateProfile.query.filter_by(user_id=user_id).first()
        if not profile:
            raise NotFoundError(f"Candidate profile for user {user_id} not found")

        return {
            "user_id": profile.user_id,
            "skills": profile.skills,
            "experience": profile.experience,
            "education": profile.education,
            "phone": profile.phone,
            "linkedin": profile.linkedin,
            "updated_at": profile.updated_at.isoformat(),
        }

    @staticmethod
    def process_and_store_cv(user_id: int, file_path: str) -> dict:
        """Process CV file and store parsed data.

        Args:
            user_id: User ID
            file_path: Path to CV file

        Returns:
            Dictionary with parsed CV data

        Raises:
            NotFoundError: If user not found
        """
        user = User.query.get(user_id)
        if not user:
            raise NotFoundError(f"User {user_id} not found")

        # Extract text from PDF
        text = extract_text(file_path)

        # Parse CV with NLP
        parsed = parse_cv(text)

        # Get or create candidate profile
        profile = CandidateProfile.query.filter_by(user_id=user_id).first()
        if not profile:
            profile = CandidateProfile(user_id=user_id)
            db.session.add(profile)

        # Update profile with parsed data
        profile.skills = parsed.get("skills")
        profile.experience = parsed.get("experience")
        profile.education = parsed.get("education")
        profile.cv_text = text
        profile.cv_path = file_path

        db.session.commit()

        return parsed

    @staticmethod
    def get_all_candidates_for_ranking() -> list:
        """Get all candidates with CV text for ranking.

        Returns:
            List of candidate dictionaries with cv_text
        """
        profiles = CandidateProfile.query.filter(
            CandidateProfile.cv_text.isnot(None)
        ).all()

        candidates = []
        for profile in profiles:
            candidates.append({
                "user_id": profile.user_id,
                "skills": profile.skills,
                "experience": profile.experience,
                "education": profile.education,
                "text": profile.cv_text,
            })

        return candidates
