"""Ranking service with strategy pattern for algorithm selection."""
from app.schemas import RankingRequestSchema
from app.services.ranking import tfidf, semantic
from app.utils import ValidationError, BadRequestError


class RankingService:
    """Service for ranking candidates using strategy pattern."""

    @staticmethod
    def rank_candidates(job_description: str, candidates: list, method: str = "tfidf") -> list:
        """Rank candidates against job description.

        Uses strategy pattern to select between TF-IDF and semantic ranking algorithms.

        Args:
            job_description: Job description text
            candidates: List of candidate dictionaries with 'text' field
            method: Ranking method - 'tfidf' or 'semantic'

        Returns:
            List of ranked candidates with scores

        Raises:
            ValidationError: If data is invalid
            BadRequestError: If ranking fails
        """
        # Validate input
        schema = RankingRequestSchema(job_description=job_description, method=method)
        try:
            schema.validate()
        except ValueError as e:
            raise ValidationError(str(e))

        # Validate candidates
        if not candidates:
            return []

        try:
            # Select ranking strategy
            if method == "semantic":
                ranked = semantic.rank_candidates_semantic(job_description, candidates)
            elif method == "tfidf":
                ranked = tfidf.rank_candidates_tfidf(job_description, candidates)
            else:
                raise ValueError(f"Unknown ranking method: {method}")

            return ranked
        except Exception as e:
            raise BadRequestError(f"Ranking failed: {str(e)}")

    @staticmethod
    def get_available_methods() -> list:
        """Get list of available ranking methods.

        Returns:
            List of available ranking method names
        """
        return ["tfidf", "semantic"]
