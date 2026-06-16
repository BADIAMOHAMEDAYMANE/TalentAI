# TalentAI Architecture Quick Reference

## Project Structure at a Glance

```
backend/
├── app/
│   ├── __init__.py                      # Flask app factory
│   │
│   ├── models/                          # Database models
│   │   ├── __init__.py                 # Exports: User, Job, CandidateProfile, Application
│   │   ├── user.py                     # User(id, name, email, password, role)
│   │   ├── job.py                      # Job(id, title, description, location, salary, experience)
│   │   ├── candidate_profile.py        # CandidateProfile(id, user_id, skills, experience, education, cv_text, cv_path)
│   │   └── application.py              # Application(id, candidate_id, job_id, status, score, applied_at)
│   │
│   ├── routes/                          # API endpoints (thin controllers)
│   │   ├── auth.py                     # POST /api/auth/register, POST /api/auth/login
│   │   ├── cv.py                       # POST /api/cv/upload, POST /api/cv/rank
│   │   ├── jobs.py                     # CRUD /api/jobs
│   │   ├── candidates.py               # GET /api/candidates/{id}
│   │   └── applications.py             # CRUD /api/applications
│   │
│   ├── services/                        # Business logic layer
│   │   ├── __init__.py                 # Exports all services
│   │   ├── auth_service.py             # register_user(), authenticate_user()
│   │   ├── candidate_service.py        # CV upload, parsing, retrieval
│   │   ├── job_service.py              # Job CRUD operations
│   │   ├── application_service.py      # Application management
│   │   ├── ranking_service.py          # Ranking algorithm selection (strategy pattern)
│   │   │
│   │   ├── parser/                     # CV parsing services
│   │   │   ├── extractor.py           # extract_text(pdf_path) → text
│   │   │   └── nlp.py                 # parse_cv(text) → {name, skills, experience, education}
│   │   │
│   │   └── ranking/                    # Ranking algorithms
│   │       ├── semantic.py            # rank_candidates_semantic() via sentence-transformers
│   │       └── tfidf.py               # rank_candidates_tfidf() via scikit-learn
│   │
│   ├── schemas/                         # Request/response validation & DTOs
│   │   ├── __init__.py                 # Exports all schemas
│   │   ├── user_schema.py              # UserRegisterSchema, UserLoginSchema, UserResponseSchema
│   │   ├── job_schema.py               # JobCreateSchema, JobResponseSchema
│   │   ├── candidate_schema.py         # CandidateProfileSchema, RankingRequestSchema
│   │   └── application_schema.py       # ApplicationCreateSchema, ApplicationUpdateSchema
│   │
│   └── utils/                           # Utilities
│       ├── __init__.py                 # Exports all utilities
│       ├── errors.py                   # Custom exceptions (ValidationError, NotFoundError, etc)
│       ├── decorators.py               # @role_required, @candidate_or_admin, @recruiter_or_admin
│       └── helpers.py                  # hash_password(), get_current_user(), format_response()
│
├── config.py                            # Configuration classes (Dev, Prod, Test)
├── run.py                               # Application entry point
└── requirements.txt                     # Dependencies
```

---

## Data Flow

### User Registration
```
POST /api/auth/register
  → auth.py (route)
    → AuthService.register_user()
      → UserRegisterSchema.validate()
      → User.create() [ORM]
      → return user_dict
  ← 201 Created
```

### CV Upload & Parsing
```
POST /api/cv/upload (JWT required)
  → cv.py (route)
    → CandidateService.process_and_store_cv()
      → extract_text() [PDF → Text]
      → parse_cv() [NLP parsing]
      → CandidateProfile.create() [ORM]
      → return parsed_data
  ← 201 Created
```

### Candidate Ranking
```
POST /api/cv/rank (JWT required)
  → cv.py (route)
    → CandidateService.get_all_candidates_for_ranking()
    → RankingService.rank_candidates()
      → TF-IDF or Semantic ranking [algorithm selection]
      ← scored_candidates
  ← 200 OK with ranking results
```

---

## Key Service Classes

### AuthService
```python
class AuthService:
    @staticmethod
    def register_user(data: dict) -> dict
        # Validates, hashes password, creates User, returns user_dict
    
    @staticmethod
    def authenticate_user(email: str, password: str) -> dict
        # Verifies credentials, creates JWT token, returns token + user
```

### CandidateService
```python
class CandidateService:
    @staticmethod
    def get_candidate_profile(user_id: int) -> dict
        # Returns candidate profile from database
    
    @staticmethod
    def process_and_store_cv(user_id: int, file_path: str) -> dict
        # Extract text → Parse NLP → Store in database
    
    @staticmethod
    def get_all_candidates_for_ranking() -> list
        # Returns all candidates with CV text for ranking
```

### JobService
```python
class JobService:
    @staticmethod
    def create_job(recruiter_id: int, data: dict) -> dict
    
    @staticmethod
    def get_job(job_id: int) -> dict
    
    @staticmethod
    def list_jobs(limit: int = 50, offset: int = 0) -> list
    
    @staticmethod
    def delete_job(job_id: int, recruiter_id: int) -> bool
```

### RankingService (Strategy Pattern)
```python
class RankingService:
    @staticmethod
    def rank_candidates(job_description: str, candidates: list, method: str) -> list
        # Routes to semantic.py or tfidf.py based on method parameter
```

---

## Decorators & Error Handling

### Role-Based Access Control
```python
@role_required("recruiter", "admin")        # Only recruiters and admins
def create_job():
    ...

@candidate_or_admin                         # Only candidates and admins
def upload_cv():
    ...

@recruiter_or_admin                         # Only recruiters and admins
def update_application():
    ...
```

### Custom Exceptions
```python
raise ValidationError("Invalid email")      # 400 Bad Request
raise AuthenticationError("Wrong password")  # 401 Unauthorized
raise AuthorizationError("Access denied")   # 403 Forbidden
raise NotFoundError("User not found")       # 404 Not Found
raise ConflictError("Email already exists") # 409 Conflict
```

---

## Configuration

### Environment Variables
```bash
FLASK_ENV=development                      # development | production | testing
DEBUG=False                                 # Flask debug mode
SQLALCHEMY_DATABASE_URI=...                 # Database connection
JWT_SECRET_KEY=...                          # JWT secret key
EMBEDDING_MODEL_NAME=...                    # Sentence transformer model
SPACY_MODEL_NAME=...                        # spaCy model name
```

### Config Classes
- `DevelopmentConfig` - Debug=True, Echo SQL logs
- `ProductionConfig` - Debug=False, Requires JWT_SECRET_KEY env var
- `TestingConfig` - In-memory SQLite database

---

## API Endpoints

| Method | Endpoint | Auth | Handler | Service |
|--------|----------|------|---------|---------|
| POST | /api/auth/register | ❌ | auth.register() | AuthService |
| POST | /api/auth/login | ❌ | auth.login() | AuthService |
| POST | /api/cv/upload | ✅ | cv.upload_cv() | CandidateService |
| POST | /api/cv/rank | ✅ | cv.rank_candidates() | RankingService |
| POST | /api/jobs | ✅ recruiter | jobs.create_job() | JobService |
| GET | /api/jobs | ❌ | jobs.list_jobs() | JobService |
| GET | /api/jobs/{id} | ❌ | jobs.get_job() | JobService |
| DELETE | /api/jobs/{id} | ✅ recruiter | jobs.delete_job() | JobService |
| GET | /api/candidates/me | ✅ | candidates.get_my_profile() | CandidateService |
| GET | /api/candidates/{id} | ❌ | candidates.get_candidate_profile() | CandidateService |
| POST | /api/applications | ✅ candidate | applications.create_application() | ApplicationService |
| PATCH | /api/applications/{id} | ✅ recruiter | applications.update_application_status() | ApplicationService |

---

## Adding New Features

### Example: Add a new endpoint

1. **Create Service Method** (e.g., in `job_service.py`)
   ```python
   @staticmethod
   def search_jobs(keyword: str) -> list:
       # Business logic here
       return results
   ```

2. **Create Route** (e.g., in `routes/jobs.py`)
   ```python
   @jobs_bp.get("/search")
   def search(keyword):
       try:
           results = JobService.search_jobs(keyword)
           return jsonify(results), 200
       except Exception as e:
           return format_error_response(str(e), 500)
   ```

3. **Register Blueprint** (already done in `app/__init__.py`)
   - Blueprints are auto-registered with their prefixes

4. **Add Schema** (if needed validation)
   ```python
   # In schemas/job_schema.py
   @dataclass
   class JobSearchSchema:
       keyword: str
       def validate(self):
           if not self.keyword:
               raise ValueError("Keyword required")
   ```

---

## Testing

### Import Test
```bash
python -c "from app import create_app; app = create_app(); print('✅ OK')"
```

### Model Test
```bash
python -c "from app.models import User, Job, CandidateProfile, Application; print('✅ OK')"
```

### Service Test
```bash
python -c "from app.services import AuthService, JobService; print('✅ OK')"
```

### Run Application
```bash
cd backend
python run.py
# Server runs on http://127.0.0.1:5000
```

---

## Files to Know

| File | Purpose |
|------|---------|
| `app/__init__.py` | Flask app factory, blueprint registration |
| `config.py` | Configuration classes |
| `app/models/` | SQLAlchemy models (separate files) |
| `app/routes/` | API endpoints (thin controllers) |
| `app/services/` | Business logic layer |
| `app/schemas/` | Request/response validation |
| `app/utils/` | Utilities, errors, decorators |

---

## Common Patterns

### Service Method Template
```python
@staticmethod
def operation_name(param1, param2):
    """Brief description."""
    try:
        # Validate input with schema
        schema = SomeSchema(param1=param1, param2=param2)
        schema.validate()
        
        # Business logic
        result = Model.query.filter_by(...).first()
        if not result:
            raise NotFoundError("Not found")
        
        # Return formatted response
        return result.to_dict()
    
    except ValidationError as e:
        raise ValidationError(str(e))
    except NotFoundError:
        raise
```

### Route Handler Template
```python
@bp.post("/endpoint")
@jwt_required()  # if needed
def handle_request():
    try:
        user = get_current_user()
        data = request.get_json()
        
        result = Service.operation(data)
        return jsonify(result), 200
    
    except ValidationError as e:
        return format_error_response(str(e), 400)
    except NotFoundError as e:
        return format_error_response(str(e), 404)
    except Exception as e:
        return format_error_response(f"Error: {str(e)}", 500)
```

---

## Performance Tips

1. **Database Queries**
   - Use `filter_by()` for simple queries
   - Use `filter()` for complex queries
   - Add pagination with `.offset().limit()`

2. **Caching**
   - Consider Redis for frequently accessed data
   - Cache ranking results if job descriptions don't change

3. **Async Operations**
   - Consider Celery for long-running CV parsing
   - Use async job queue for ranking large candidate sets

---

## Next Steps

1. Write unit tests for services
2. Add API documentation (Swagger)
3. Set up logging
4. Configure error tracking (Sentry)
5. Add database migrations (Alembic)
6. Set up CI/CD pipeline
