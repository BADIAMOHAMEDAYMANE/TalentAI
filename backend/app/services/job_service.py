"""Job management service."""
from app import db
from app.models import Job, User
from app.schemas import JobCreateSchema
from app.utils import NotFoundError, ValidationError


class JobService:
    """Service for job management."""

    @staticmethod
    def create_job(recruiter_id: int, data: dict) -> dict:
        """Create a new job posting.

        Args:
            recruiter_id: ID of recruiter creating the job
            data: Dictionary with title, description, location, salary, experience

        Returns:
            Dictionary with created job data

        Raises:
            ValidationError: If data is invalid
            NotFoundError: If recruiter not found
        """
        # Verify recruiter exists
        recruiter = User.query.get(recruiter_id)
        if not recruiter:
            raise NotFoundError(f"Recruiter with id {recruiter_id} not found")

        schema = JobCreateSchema(**data)
        schema.validate()

        job = Job(
            title=schema.title,
            description=schema.description,
            location=schema.location,
            salary=schema.salary,
            experience=schema.experience,
            recruiter_id=recruiter_id,
        )
        db.session.add(job)
        db.session.commit()

        return {
            "id": job.id,
            "title": job.title,
            "description": job.description,
            "location": job.location,
            "salary": job.salary,
            "experience": job.experience,
            "recruiter_id": job.recruiter_id,
            "created_at": job.created_at.isoformat(),
        }

    @staticmethod
    def get_job(job_id: int) -> dict:
        """Get job by ID.

        Args:
            job_id: Job ID

        Returns:
            Dictionary with job data

        Raises:
            NotFoundError: If job not found
        """
        job = Job.query.get(job_id)
        if not job:
            raise NotFoundError(f"Job with id {job_id} not found")

        return {
            "id": job.id,
            "title": job.title,
            "description": job.description,
            "location": job.location,
            "salary": job.salary,
            "experience": job.experience,
            "recruiter_id": job.recruiter_id,
            "created_at": job.created_at.isoformat(),
        }

    @staticmethod
    def list_jobs(limit: int = 50, offset: int = 0) -> list:
        """List all jobs with pagination.

        Args:
            limit: Number of jobs to return
            offset: Number of jobs to skip

        Returns:
            List of job dictionaries
        """
        jobs = Job.query.offset(offset).limit(limit).all()

        return [
            {
                "id": job.id,
                "title": job.title,
                "description": job.description,
                "location": job.location,
                "salary": job.salary,
                "experience": job.experience,
                "recruiter_id": job.recruiter_id,
                "created_at": job.created_at.isoformat(),
            }
            for job in jobs
        ]

    @staticmethod
    def delete_job(job_id: int, recruiter_id: int) -> bool:
        """Delete a job (only recruiter who created it can delete).

        Args:
            job_id: Job ID
            recruiter_id: ID of recruiter deleting the job

        Returns:
            True if deleted

        Raises:
            NotFoundError: If job not found
            ValidationError: If recruiter is not the owner
        """
        job = Job.query.get(job_id)
        if not job:
            raise NotFoundError(f"Job with id {job_id} not found")

        if job.recruiter_id != recruiter_id:
            raise ValidationError("You can only delete jobs you created")

        db.session.delete(job)
        db.session.commit()
        return True
