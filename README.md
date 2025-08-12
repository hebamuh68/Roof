# Roof - Apartment Search Platform

A FastAPI-based apartment search platform with Elasticsearch integration.

## Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL
- Elasticsearch

### Installation

1. **Clone and setup**
   ```bash
   git clone <repository-url>
   cd Roof
   python -m venv .venv
   source .venv/bin/activate
   pip install fastapi uvicorn sqlalchemy psycopg2-binary elasticsearch alembic pydantic
   ```

2. **Environment setup**
   Create `.env` file:
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/roof_db
   ELASTIC_URL=http://localhost:9200
   ```

3. **Database setup**
   ```bash
   alembic upgrade head
   python app/seed.py
   ```

4. **Elasticsearch setup**
   ```bash
   python app/services/elasticsearch_setup.py
   python app/utils/es_indexer.py
   ```

5. **Run the app**
   ```bash
   uvicorn app.main:app --reload
   ```

## API Endpoints

### Search Apartments
```
GET /search/apartments?query={search_term}
```

**Example:**
```bash
curl "http://localhost:8000/search/apartments?query=Cairo"
```

## Project Structure

```
Roof/
├── app/
│   ├── api/              # API routes
│   ├── database/         # Database config
│   ├── models/           # Pydantic models
│   ├── schemas/          # SQLAlchemy models
│   ├── services/         # Business logic
│   └── utils/            # Utilities
├── alembic/              # Database migrations
└── main.py               # App entry point
```

## Database Schema

### Users
- `id`, `first_name`, `last_name`, `email`, `location`
- `flatmate_pref`, `keywords` (arrays)

### Apartments
- `id`, `title`, `description`, `location`, `apartment_type`
- `rent_per_week`, `start_date`, `duration_len`
- `place_accept`, `furnishing_type`, `is_pathroom_solo`
- `parking_type`, `keywords`, `is_active`

## Development

### Add new features
1. Update models in `app/models/` and `app/schemas/`
2. Create migration: `alembic revision --autogenerate -m "Description"`
3. Apply: `alembic upgrade head`
4. Add API routes in `app/api/`

### Test Elasticsearch
```python
from elasticsearch import Elasticsearch
es = Elasticsearch("http://localhost:9200")
print(es.info())
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string |
| `ELASTIC_URL` | Elasticsearch server URL |