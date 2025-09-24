# Roof - Mac Setup Guide

This guide will help you set up the Roof project on macOS.

## Prerequisites

- macOS (tested on macOS Sequoia 15.3.0)
- Homebrew package manager
- Git

## Quick Setup

Run the automated setup script:

```bash
./setup-mac.sh
```

This script will:
- Install required dependencies (Node.js, pnpm, PostgreSQL)
- Set up Python virtual environment
- Install Python dependencies
- Configure database
- Run migrations
- Install frontend dependencies
- Test the setup

## Manual Setup

If you prefer to set up manually or the script fails:

### 1. Install Dependencies

```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Node.js and pnpm
brew install node
npm install -g pnpm

# Install PostgreSQL
brew install postgresql@14
brew services start postgresql@14
```

### 2. Set Up Database

```bash
# Create database
createdb roof_db
```

### 3. Set Up Backend

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r backend/requirements-py39.txt

# Configure environment
cp backend/env.example backend/.env
# Edit backend/.env with your database credentials
```

### 4. Run Migrations

```bash
source .venv/bin/activate
alembic upgrade head
```

### 5. Set Up Frontend

```bash
cd frontend
pnpm install
cd ..
```

## Running the Application

### Backend

```bash
cd backend
source ../.venv/bin/activate
uvicorn app.main:app --reload
```

Backend will be available at: http://localhost:8000
API documentation: http://localhost:8000/docs

### Frontend

```bash
cd frontend
pnpm run dev
```

Frontend will be available at: http://localhost:5173

## Troubleshooting

### Python Version Issues

The project is configured for Python 3.9. If you have a different version:

1. Install Python 3.9 via Homebrew: `brew install python@3.9`
2. Use the specific version: `python3.9 -m venv .venv`

### PostgreSQL Connection Issues

If you get connection errors:

1. Make sure PostgreSQL is running: `brew services start postgresql@14`
2. Check your database URL in `backend/.env`
3. Ensure the database exists: `createdb roof_db`

### Import Errors

If you get module import errors:

1. Make sure you're in the correct directory
2. Activate the virtual environment: `source .venv/bin/activate`
3. Check that all dependencies are installed

### Frontend Build Issues

If the frontend build fails:

1. Make sure `tsconfig.vitest.json` exists (created by setup script)
2. Check Node.js version compatibility
3. Clear node_modules and reinstall: `rm -rf node_modules && pnpm install`

## Project Structure

```
ROOF/
├── backend/             # FastAPI backend
│   ├── app/
│   │   ├── api/         # API endpoints
│   │   ├── models/      # Pydantic models
│   │   ├── schemas/     # SQLAlchemy models
│   │   ├── services/    # Business logic
│   │   └── utils/       # Utilities
│   ├── requirements-py39.txt  # Python dependencies for Python 3.9
│   └── .env            # Environment configuration
├── frontend/            # Vue.js frontend
│   ├── src/
│   │   ├── components/  # Vue components
│   │   ├── views/       # Page components
│   │   ├── stores/      # Pinia stores
│   │   └── router/      # Vue Router
│   └── public/          # Static assets
├── alembic/             # Database migrations
├── .venv/               # Python virtual environment
└── setup-mac.sh         # Mac setup script
```

## Environment Variables

Key environment variables in `backend/.env`:

```env
DATABASE_URL=postgresql://your_username@localhost:5432/roof_db
ELASTIC_URL=http://localhost:9200
ELASTIC_USER=elastic
ELASTIC_PASSWORD=changeme
SECRET_KEY=your_secret_key_here
```

## Development Tips

1. **Virtual Environment**: Always activate the virtual environment before working on the backend:
   ```bash
   source .venv/bin/activate
   ```

2. **Database Migrations**: After making schema changes:
   ```bash
   alembic revision --autogenerate -m "Description of changes"
   alembic upgrade head
   ```

3. **Frontend Development**: The frontend uses Vite for fast development with hot reload.

4. **API Testing**: Use the Swagger UI at http://localhost:8000/docs for testing API endpoints.

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Ensure all dependencies are properly installed
3. Verify your environment configuration
4. Check the logs for specific error messages
