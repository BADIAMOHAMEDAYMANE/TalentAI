from datetime import datetime
from app import db


class User(db.Model):
    """User model for candidates and recruiters."""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default="candidate")  # candidate | recruiter | admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    profile = db.relationship("CandidateProfile", backref="user", uselist=False)
    applications = db.relationship("Application", backref="candidate")

    def __repr__(self):
        return f"<User {self.email}>"
