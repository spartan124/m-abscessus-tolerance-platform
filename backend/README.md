# M. abscessus Tolerance Platform - Backend

FastAPI-based REST API for the M. abscessus antibiotic tolerance research platform.

## Setup

### Prerequisites
- Python 3.11+
- PostgreSQL 13+
- MongoDB 6+

### Local Development

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your database credentials
uvicorn app.main:app --reload
```

### API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Running Tests

```bash
pytest tests/ -v --cov=app
```

## Project Structure

```
backend/
├── app/
│   ├── main.py          # FastAPI app entry point
│   ├── config.py        # Configuration via environment variables
│   ├── database.py      # PostgreSQL (SQLAlchemy) + MongoDB (Motor)
│   ├── security.py      # JWT auth + password hashing
│   ├── api/             # Route handlers
│   ├── models/          # SQLAlchemy ORM models
│   ├── schemas/         # Pydantic request/response schemas
│   ├── services/        # Business logic & data processing
│   ├── utils/           # Helper functions
│   └── middleware/      # Custom middleware
└── tests/               # Pytest test suite
```
