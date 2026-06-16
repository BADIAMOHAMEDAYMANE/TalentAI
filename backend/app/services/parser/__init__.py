"""Parser services for CV text extraction and NLP processing."""
from app.services.parser.extractor import extract_text
from app.services.parser.nlp import parse_cv

__all__ = ["extract_text", "parse_cv"]
