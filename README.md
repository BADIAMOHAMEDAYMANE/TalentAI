# TalentAI – Candidate Ranking System

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Flask 3.0](https://img.shields.io/badge/flask-3.0-green?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/postgresql-13%2B-blue?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/license-All%20Rights%20Reserved-red)](LICENSE)
[![Status](https://img.shields.io/badge/status-Active-brightgreen)](https://github.com)
[![Code Style](https://img.shields.io/badge/code%20style-PEP8-purple)](https://www.python.org/dev/peps/pep-0008/)

An intelligent recruitment platform that automatically parses CVs, extracts skills, and ranks candidates based on job descriptions using machine learning.

---

## 🎯 Key Features

[![JWT Auth](https://img.shields.io/badge/Authentication-JWT-orange?logo=jsonwebtokens&logoColor=white)](https://jwt.io/)
[![ML Ranking](https://img.shields.io/badge/Ranking-ML%2BSemantics-blueviolet?logo=tensorflow&logoColor=white)](https://www.tensorflow.org/)
[![PDF Processing](https://img.shields.io/badge/PDF-Text%20Extraction-red?logo=adobeacrobatreader&logoColor=white)](https://pdfplumber.readthedocs.io/)
[![NLP](https://img.shields.io/badge/NLP-spaCy-lightblue?logo=spacy&logoColor=white)](https://spacy.io/)
[![REST API](https://img.shields.io/badge/API-REST%20JSON-yellowgreen?logo=fastapi&logoColor=white)](https://www.jsonapis.org/)
[![ORM](https://img.shields.io/badge/Database-SQLAlchemy-orange?logo=sqlite&logoColor=white)](https://www.sqlalchemy.org/)

---

```
TalentAI/
├── backend/                          # Flask REST API server
│   ├── app/                          # Application package
│   │   ├── __init__.py              # Flask app factory, JWT & DB initialization
│   │   ├── models.py                # SQLAlchemy ORM models (User, Job, CandidateProfile, Application)
│   │   ├── routes/                  # API endpoints
│   │   │   ├── auth.py              # Authentication (register, login)
│   │   │   └── cv.py                # CV upload & candidate ranking
│   │   └── services/                # Business logic layer
│   │       ├── parser/              # CV parsing & text extraction
│   │       │   ├── extractor.py     # PDF text extraction (pdfplumber)
│   │       │   ├── nlp.py           # NLP processing with spaCy
│   │       │   └── normalize.py     # Text normalization
│   │       └── ranking/             # Candidate ranking algorithms
│   │           ├── semantic.py      # Semantic similarity (sentence-transformers)
│   │           └── tfidf.py         # TF-IDF ranking (scikit-learn)
│   ├── config.py                    # Configuration settings (empty)
│   ├── run.py                       # Application entry point
│   ├── requirements.txt             # Python dependencies
│   └── venv/                        # Virtual environment
├── frontend/                        # Frontend application (UI)
└── README.md                        # This file
```

---

## 🏗️ Architecture Overview

### Backend Stack
- **Framework**: Flask (Python REST API)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT (Flask-JWT-Extended)
- **PDF Processing**: pdfplumber
- **NLP**: spaCy for entity recognition
- **ML Models**: 
  - sentence-transformers (semantic similarity ranking)
  - scikit-learn (TF-IDF ranking)

### Core Modules

#### 1. **Models** (`app/models.py`)
Four main entities in the system:

- **User**: Candidates and recruiters
  - Fields: id, name, email, password (hashed), role, created_at
  - Roles: `candidate`, `recruiter`, `admin`

- **Job**: Job postings created by recruiters
  - Fields: id, title, description, location, salary, experience (years required), recruiter_id, created_at

- **CandidateProfile**: Extended candidate information
  - Fields: id, user_id, skills, experience, education, cv_text, cv_path, phone, linkedin, updated_at
  - Links to: User (1:1 relationship)

- **Application**: Job applications with ranking scores
  - Fields: id, candidate_id, job_id, status, score, applied_at
  - Statuses: `applied`, `under_review`, `interview`, `accepted`, `rejected`

#### 2. **Routes** (`app/routes/`)

##### Authentication (`auth.py`)
- `POST /api/auth/register` – Create new user account
  - Body: `{name, email, password, role?}`
  - Returns: User details + validation

- `POST /api/auth/login` – Authenticate & get JWT token
  - Body: `{email, password}`
  - Returns: JWT access token + user details

##### CV Management (`cv.py`)
- `POST /api/cv/upload` – Upload and parse CV (protected)
  - Body: File upload (PDF)
  - Process: Extract text → Parse with NLP → Save to profile
  - Returns: Extracted {name, skills, experience, education}

- `POST /api/cv/rank` – Rank candidates against job description (protected)
  - Body: `{job_description, method?}` (method: "semantic" or "tfidf")
  - Process: Compare job description to candidate CVs using chosen algorithm
  - Returns: Ranked candidate list with scores

#### 3. **Services** (`app/services/`)

##### Parser (`parser/`)
- **extractor.py**: Extracts text from PDF files
  - Uses `pdfplumber` to read PDF pages
  - Cleans output: removes excessive newlines, non-ASCII characters

- **nlp.py**: Parses CV text into structured data
  - Uses spaCy's `en_core_web_sm` model
  - Extracts: name (PERSON entity), skills (keyword matching), experience (years), education level
  - Skills database: Python, SQL, React, Docker, TensorFlow, PyTorch, Kafka, Spark, JavaScript, Java, Node, AWS, Azure

- **normalize.py**: Text normalization (placeholder for future use)

##### Ranking (`ranking/`)
Two parallel ranking algorithms for candidate-job matching:

- **semantic.py**: Neural network-based semantic similarity
  - Model: `sentence-transformers/all-MiniLM-L6-v2`
  - Process: Converts job description & CV texts to embeddings → computes cosine similarity
  - Pros: Understands context & meaning, not just keywords
  - Returns: Score 0–100 (similarity percentage)

- **tfidf.py**: Statistical keyword matching
  - Algorithm: TF-IDF vectorizer + cosine similarity
  - Process: Counts term frequencies → ranks by keyword overlap
  - Pros: Fast, interpretable, language-agnostic
  - Returns: Score 0–100 (keyword match percentage)

---

## 🚀 API Endpoints

### Authentication
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/auth/register` | ❌ | Create user account |
| POST | `/api/auth/login` | ❌ | Get JWT token |

### CV & Ranking
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/cv/upload` | ✅ JWT | Upload & parse CV |
| POST | `/api/cv/rank` | ✅ JWT | Rank candidates by job description |

---

## 🔄 Data Flow

### CV Upload Flow
```
User uploads PDF
    ↓
extractor.py: Extract text from PDF
    ↓
nlp.py: Parse into {name, skills, experience, education}
    ↓
CandidateProfile: Store parsed data + raw CV text
    ↓
Return: Structured candidate profile
```

### Candidate Ranking Flow
```
Recruiter sends job_description + ranking method
    ↓
Load all CandidateProfiles from database
    ↓
Rank candidates:
  ├─ If "semantic": Use sentence-transformers for meaning-based matching
  └─ If "tfidf": Use scikit-learn for keyword-based matching
    ↓
Return: Sorted candidates with scores (100 = perfect match)
```

---

## 📦 Dependencies

[![Flask](https://img.shields.io/badge/Flask-3.0.0-green?logo=flask)](https://flask.palletsprojects.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-3.1.1-red?logo=sqlite)](https://www.sqlalchemy.org/)
[![JWT](https://img.shields.io/badge/JWT--Extended-4.5.3-orange?logo=jsonwebtokens)](https://flask-jwt-extended.readthedocs.io/)
[![pdfplumber](https://img.shields.io/badge/pdfplumber-0.10.3-red?logo=adobeacrobatreader)](https://github.com/jsvine/pdfplumber)
[![spaCy](https://img.shields.io/badge/spaCy-3.7.2-lightblue?logo=spacy)](https://spacy.io/)
[![sentence-transformers](https://img.shields.io/badge/sentence--transformers-2.2.2-blueviolet?logo=tensorflow)](https://www.sbert.net/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3.2-blue?logo=scikit-learn)](https://scikit-learn.org/)

Core packages (see `requirements.txt`):

---

## ⚙️ Setup & Installation

### 1. Install dependencies
```bash
cd backend
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 2. Configure database
Update PostgreSQL URI in `app/__init__.py`:
```python
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://user:pass@localhost/talentai"
```

### 3. Set JWT secret (production)
Change in `app/__init__.py`:
```python
app.config["JWT_SECRET_KEY"] = "your-secret-key-here"
```

### 4. Run the server
```bash
python run.py
# Server runs on http://127.0.0.1:5000
```

---

## 🔐 Security Notes

⚠️ **Current Issues**:
- JWT key is hardcoded (unsafe for production)
- Database credentials in code (use environment variables)
- No HTTPS or CORS configuration

**Improvements Needed**:
- Store secrets in `.env` file or secrets manager
- Implement CORS for frontend integration
- Add input validation & rate limiting
- Use parameterized queries (SQLAlchemy does this already)

---

## 🧪 Testing the API

### 1. Register a user
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepass",
    "role": "candidate"
  }'
```

### 2. Login & get token
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepass"
  }'
# Response: {"access_token": "eyJ0eXAi...", "user": {...}}
```

### 3. Upload CV (requires JWT token)
```bash
curl -X POST http://localhost:5000/api/cv/upload \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "cv=@resume.pdf"
```

### 4. Rank candidates
```bash
curl -X POST http://localhost:5000/api/cv/rank \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "job_description": "Looking for a Python developer with 5+ years experience in Flask and PostgreSQL",
    "method": "semantic"
  }'
```

---

## 📊 Database Schema

```sql
-- Users table
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(120) NOT NULL,
  email VARCHAR(120) UNIQUE NOT NULL,
  password VARCHAR(256) NOT NULL,
  role VARCHAR(20) DEFAULT 'candidate',
  created_at TIMESTAMP DEFAULT NOW()
);

-- Candidate profiles
CREATE TABLE candidate_profiles (
  id SERIAL PRIMARY KEY,
  user_id INTEGER UNIQUE REFERENCES users(id),
  skills JSON,
  experience INTEGER,
  education VARCHAR(50),
  cv_text TEXT,
  cv_path VARCHAR(256),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Jobs
CREATE TABLE jobs (
  id SERIAL PRIMARY KEY,
  title VARCHAR(200) NOT NULL,
  description TEXT NOT NULL,
  recruiter_id INTEGER REFERENCES users(id),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Applications
CREATE TABLE applications (
  id SERIAL PRIMARY KEY,
  candidate_id INTEGER REFERENCES users(id),
  job_id INTEGER REFERENCES jobs(id),
  status VARCHAR(30) DEFAULT 'applied',
  score FLOAT,
  applied_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🛠️ Development Notes

- **Debug mode**: Enabled by default in `run.py` (change for production)
- **Model loading**: `sentence-transformers` model loads at app startup (~5-10 seconds)
- **Spacy model**: Downloaded separately with `python -m spacy download en_core_web_sm`
- **Hot reload**: Flask's debug mode watches for file changes and restarts

---

## 📝 Future Enhancements

- [ ] Frontend integration (React/Vue)
- [ ] Job matching recommendations
- [ ] Batch candidate ranking
- [ ] Resume template parsing
- [ ] Interview scheduling
- [ ] Analytics dashboard
- [ ] Multi-language CV support
- [ ] Resume improvement suggestions

---

## 📝 License

All rights reserved. TalentAI 2026.

---

## 📊 Project Status

[![Maintenance](https://img.shields.io/badge/Maintenance-Active-brightgreen)](https://github.com)
[![Last Updated](https://img.shields.io/badge/Last%20Updated-June%202026-blue)](https://github.com)
[![Contributors](https://img.shields.io/badge/Contributors-Open-green)](CONTRIBUTING.md)
[![Issues](https://img.shields.io/badge/Issues-Report%20Here-red)](https://github.com/issues)
