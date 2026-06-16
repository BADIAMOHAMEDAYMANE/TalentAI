import spacy
import re

# Charger les deux modèles
nlp_en = spacy.load("en_core_web_sm")
nlp_fr = spacy.load("fr_core_news_sm")

SKILL_KEYWORDS = {
    "python", "sql", "react", "docker", "tensorflow", "pytorch",
    "kafka", "spark", "javascript", "java", "node", "aws", "azure"
}

def _detect_language(text: str) -> str:
    french_words = {"le", "la", "les", "de", "du", "des", "je", "mon", "par", "avec", "pour", "sur"}
    words = set(text.lower().split())
    return "fr" if len(words & french_words) > 3 else "en"

def parse_cv(text: str) -> dict:
    lang = _detect_language(text)
    nlp  = nlp_fr if lang == "fr" else nlp_en
    doc  = nlp(text)
    return {
        "name":       _extract_name(doc),
        "skills":     _extract_skills(text),
        "experience": _extract_experience(text),
        "education":  _extract_education(text),
    }

def _extract_name(doc) -> str:
    for ent in doc.ents:
        if ent.label_ == "PER" or ent.label_ == "PERSON":
            return ent.text
    return ""

def _extract_skills(text: str) -> list[str]:
    text_lower = text.lower()
    return [s for s in SKILL_KEYWORDS if s in text_lower]

def _extract_experience(text: str) -> int:
    matches = re.findall(r'(\d+)\s+an', text, re.IGNORECASE)
    matches += re.findall(r'(\d+)\s+year', text, re.IGNORECASE)
    return max((int(m) for m in matches), default=0)

def _extract_education(text: str) -> str:
    levels = {
        "PhD":      ["phd", "doctorat"],
        "Master":   ["master", "msc", "m2", "magistère"],
        "Bachelor": ["bachelor", "licence", "l3", "bsc"],
        "Associate":["associate", "bts", "dut", "but"],
    }
    text_lower = text.lower()
    for level, keywords in levels.items():
        if any(k in text_lower for k in keywords):
            return level
    return "Unknown"