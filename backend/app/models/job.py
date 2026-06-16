from datetime import datetime
from app import db


class Job(db.Model):
    """Job posting model created by recruiters."""
    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100))
    salary = db.Column(db.String(50))
    experience = db.Column(db.Integer, default=0)  # years required
    recruiter_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    applications = db.relationship("Application", backref="job")

    def __repr__(self):
        return f"<Job {self.title}>"
