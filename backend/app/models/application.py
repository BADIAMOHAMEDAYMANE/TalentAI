from datetime import datetime
from app import db


class Application(db.Model):
    """Job application with ranking score."""
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"))
    status = db.Column(db.String(30), default="applied")
    # applied | under_review | interview | accepted | rejected
    score = db.Column(db.Float)  # ranking score (0–100)
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Application candidate_id={self.candidate_id} job_id={self.job_id}>"
