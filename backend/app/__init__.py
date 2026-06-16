from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from sentence_transformers import SentenceTransformer

db  = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://aymanebadia@localhost/talentai"
    app.config["JWT_SECRET_KEY"] = "change-me-in-production"

    db.init_app(app)
    jwt.init_app(app)
    print("📥 Chargement du modèle sémantique (all-MiniLM-L6-v2)...")
    app.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    print("✅ Modèle chargé avec succès !")

    from app.routes.cv import cv_bp
    from app.routes.auth import auth_bp
    app.register_blueprint(cv_bp,   url_prefix="/api/cv")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    return app