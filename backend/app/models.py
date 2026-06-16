from datetime import datetime
from app import db

class User(db.Model):
    __tablename__ = "users"
    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(120), nullable=False)
    email      = db.Column(db.String(120), unique=True, nullable=False)
    password   = db.Column(db.String(256), nullable=False)
    role       = db.Column(db.String(20), default="candidate")  # candidate | recruiter | admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    profile     = db.relationship("CandidateProfile", backref="user", uselist=False)
    applications = db.relationship("Application", backref="candidate")


class Job(db.Model):
    __tablename__ = "jobs"
    id           = db.Column(db.Integer, primary_key=True)
    title        = db.Column(db.String(200), nullable=False)
    description  = db.Column(db.Text, nullable=False)
    location     = db.Column(db.String(100))
    salary       = db.Column(db.String(50))
    experience   = db.Column(db.Integer, default=0)   # years required
    recruiter_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

    applications = db.relationship("Application", backref="job")


class CandidateProfile(db.Model):
    __tablename__ = "candidate_profiles"
    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True)
    skills     = db.Column(db.JSON)        # ["Python", "SQL", "Docker"]
    experience = db.Column(db.Integer)     # years
    education  = db.Column(db.String(50))
    cv_text    = db.Column(db.Text)        # raw extracted text for ranking
    cv_path    = db.Column(db.String(256)) # file path or S3 URL
    phone      = db.Column(db.String(20))
    linkedin   = db.Column(db.String(200))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Application(db.Model):
    __tablename__ = "applications"
    id           = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    job_id       = db.Column(db.Integer, db.ForeignKey("jobs.id"))
    status       = db.Column(db.String(30), default="applied")
    # applied | under_review | interview | accepted | rejected
    score        = db.Column(db.Float)     # ranking score (0–100)
    applied_at   = db.Column(db.DateTime, default=datetime.utcnow)