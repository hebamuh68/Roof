# Roof Backend

A FastAPI-based backend for the Roof apartment sharing platform.

## Setup

### Prerequisites
- Python 3.11+
- PostgreSQL/MySQL/SQLite database
- Elasticsearch (for search functionality)

### Installation

1. **Activate the virtual environment:**
   ```bash
   source ../.venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   uv pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp env.example .env
   # Edit .env with your actual values
   ```

4. **Set up database:**
   - Create your database
   - Update DATABASE_URL in .env
   - Run migrations: `alembic upgrade head`

5. **Set up Elasticsearch:**
   - Start Elasticsearch service
   - Update ELASTIC_URL, ELASTIC_USER, ELASTIC_PASSWORD in .env

## Running the Application

### Development Mode
```bash
# Option 1: Use the run script
./run.sh

# Option 2: Manual command
source ../.venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode
```bash
source ../.venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
backend/
├── app/
│   ├── api/           # API endpoints
│   ├── database/      # Database configuration
│   ├── models/        # Pydantic models
│   ├── schemas/       # SQLAlchemy models
│   ├── services/      # Business logic
│   └── utils/         # Utility functions
├── alembic/           # Database migrations
├── requirements.txt   # Python dependencies
├── run.sh            # Run script
└── env.example       # Environment variables template
```

## Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_user_api.py
```

## Code Quality

```bash
# Format code
black .

# Lint code
flake8 .

# Type checking
mypy .
```

## Next Steps

- [ ] Add comprehensive test suite
- [ ] Implement authentication & authorization
- [ ] Add input validation & error handling
- [ ] Set up logging system
- [ ] Add health check endpoints
- [ ] Implement rate limiting
- [ ] Add API documentation
- [ ] Set up CI/CD pipeline 