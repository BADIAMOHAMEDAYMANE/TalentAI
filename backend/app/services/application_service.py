"""Job application management service."""
from app import db
from app.models import Application, User, Job
from app.schemas import ApplicationCreateSchema, ApplicationUpdateSchema
from app.utils import NotFoundError, ValidationError


class ApplicationService:
    """Service for managing job applications."""

    @staticmethod
    def create_application(data: dict) -> dict:
        """Create a new job application.

        Args:
            data: Dictionary with candidate_id, job_id, score

        Returns:
            Dictionary with created application data

        Raises:
            ValidationError: If data is invalid
            NotFoundError: If candidate or job not found
        """
        schema = ApplicationCreateSchema(**data)
        schema.validate()

        # Verify candidate exists
        candidate = User.query.get(schema.candidate_id)
        if not candidate:
            raise NotFoundError(f"Candidate with id {schema.candidate_id} not found")

        # Verify job exists
        job = Job.query.get(schema.job_id)
        if not job:
            raise NotFoundError(f"Job with id {schema.job_id} not found")

        application = Application(
            candidate_id=schema.candidate_id,
            job_id=schema.job_id,
            score=schema.score,
        )
        db.session.add(application)
        db.session.commit()

        return {
            "id": application.id,
            "candidate_id": application.candidate_id,
            "job_id": application.job_id,
            "status": application.status,
            "score": application.score,
            "applied_at": application.applied_at.isoformat(),
        }

    @staticmethod
    def get_application(application_id: int) -> dict:
        """Get application by ID.

        Args:
            application_id: Application ID

        Returns:
            Dictionary with application data

        Raises:
            NotFoundError: If application not found
        """
        application = Application.query.get(application_id)
        if not application:
            raise NotFoundError(f"Application with id {application_id} not found")

        return {
            "id": application.id,
            "candidate_id": application.candidate_id,
            "job_id": application.job_id,
            "status": application.status,
            "score": application.score,
            "applied_at": application.applied_at.isoformat(),
        }

    @staticmethod
    def update_application_status(application_id: int, data: dict) -> dict:
        """Update application status.

        Args:
            application_id: Application ID
            data: Dictionary with status

        Returns:
            Dictionary with updated application data

        Raises:
            NotFoundError: If application not found
            ValidationError: If status is invalid
        """
        schema = ApplicationUpdateSchema(**data)
        schema.validate()

        application = Application.query.get(application_id)
        if not application:
            raise NotFoundError(f"Application with id {application_id} not found")

        application.status = schema.status
        db.session.commit()

        return {
            "id": application.id,
            "candidate_id": application.candidate_id,
            "job_id": application.job_id,
            "status": application.status,
            "score": application.score,
            "applied_at": application.applied_at.isoformat(),
        }

    @staticmethod
    def list_applications_for_job(job_id: int) -> list:
        """List all applications for a job.

        Args:
            job_id: Job ID

        Returns:
            List of application dictionaries
        """
        applications = Application.query.filter_by(job_id=job_id).all()

        return [
            {
                "id": app.id,
                "candidate_id": app.candidate_id,
                "job_id": app.job_id,
                "status": app.status,
                "score": app.score,
                "applied_at": app.applied_at.isoformat(),
            }
            for app in applications
        ]

    @staticmethod
    def list_applications_for_candidate(candidate_id: int) -> list:
        """List all applications from a candidate.

        Args:
            candidate_id: Candidate user ID

        Returns:
            List of application dictionaries
        """
        applications = Application.query.filter_by(candidate_id=candidate_id).all()

        return [
            {
                "id": app.id,
                "candidate_id": app.candidate_id,
                "job_id": app.job_id,
                "status": app.status,
                "score": app.score,
                "applied_at": app.applied_at.isoformat(),
            }
            for app in applications
        ]
