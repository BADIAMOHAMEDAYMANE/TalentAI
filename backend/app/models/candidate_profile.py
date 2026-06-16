from datetime import datetime
from app import db


class CandidateProfile(db.Model):
    """Extended candidate profile with parsed CV data."""
    __tablename__ = "candidate_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True)
    skills = db.Column(db.JSON)  # ["Python", "SQL", "Docker"]
    experience = db.Column(db.Integer)  # years
    education = db.Column(db.String(50))
    cv_text = db.Column(db.Text)  # raw extracted text for ranking
    cv_path = db.Column(db.String(256))  # file path or S3 URL
    phone = db.Column(db.String(20))
    linkedin = db.Column(db.String(200))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<CandidateProfile user_id={self.user_id}>"
