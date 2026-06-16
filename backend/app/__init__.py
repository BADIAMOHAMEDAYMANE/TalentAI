"""Flask application factory and extensions initialization."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from sentence_transformers import SentenceTransformer

# Initialize extensions (deferred initialization)
db = SQLAlchemy()
jwt = JWTManager()


def create_app(config_name=None):
    """Create and configure Flask application.

    Args:
        config_name: Configuration name (development, production, testing)

    Returns:
        Configured Flask application instance
    """
    from config import get_config

    app = Flask(__name__)

    # Load configuration
    config = get_config(config_name)
    app.config.from_object(config)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    # Load embedding model for semantic ranking
    print("📥 Loading semantic model (all-MiniLM-L6-v2)...")
    try:
        app.embedding_model = SentenceTransformer(app.config["EMBEDDING_MODEL_NAME"])
        print("✅ Semantic model loaded successfully!")
    except Exception as e:
        print(f"⚠️  Failed to load semantic model: {str(e)}")
        app.embedding_model = None

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.cv import cv_bp
    from app.routes.jobs import jobs_bp
    from app.routes.candidates import candidates_bp
    from app.routes.applications import applications_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(cv_bp, url_prefix="/api/cv")
    app.register_blueprint(jobs_bp, url_prefix="/api/jobs")
    app.register_blueprint(candidates_bp, url_prefix="/api/candidates")
    app.register_blueprint(applications_bp, url_prefix="/api/applications")

    return app
