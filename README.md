# Roof - Online Rental App
<img width="1510" height="1869" alt="Full project (1)" src="https://github.com/user-attachments/assets/6c11a23e-8cf4-452d-bf70-2b9070b7c31d" />


## Project Structure

```
ROOF/
├── backend/             # FastAPI backend
│   └── app/
│       ├── api/         # API endpoints
│       ├── models/      # Pydantic models (*_pyd.py)
│       ├── schemas/     # SQLAlchemy models (*_sql.py)
│       ├── services/    # Business logic
│       └── utils/       # Utilities
├── frontend/            # Vue.js frontend
│   ├── src/
│   │   ├── components/  # Vue components
│   │   ├── views/       # Page components
│   │   ├── stores/      # Pinia stores
│   │   └── router/      # Vue Router
│   └── public/          # Static assets
├── alembic/             # Database migrations
└── .venv/               # Python virtual environment
```

## Quick Start

### Backend Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your database and Elasticsearch credentials

# Database setup
alembic upgrade head
python backend/app/seed.py

# Elasticsearch setup
python backend/app/services/elasticsearch_setup.py
python backend/app/utils/es_indexer.py

# Run backend
cd backend
uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/apartments` | List apartments with pagination |
| GET | `/apartments/{id}` | Get apartment by ID |
| POST | `/apartments` | Create new apartment |
| GET | `/search/apartments` | Search apartments |
| POST | `/filter/apartments` | Filter apartments |
| GET | `/users` | List users |
| GET | `/users/{id}` | Get user by ID |
| POST | `/users` | Create new user |

## Environment Variables

```env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/roof_db

# Elasticsearch
ELASTIC_URL=https://localhost:9200
ELASTIC_USER=your_username
ELASTIC_PASSWORD=your_password
```

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL, Elasticsearch
- **Frontend**: Vue 3, TypeScript, Vite, Pinia, Vue Router
- **Database**: PostgreSQL with Alembic migrations
- **Search**: Elasticsearch for advanced search and filtering
