#!/bin/bash

# Roof Project Setup Script for Mac
# This script sets up the Roof project on macOS

set -e  # Exit on any error

echo "🏠 Setting up Roof project on Mac..."

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew is not installed. Please install Homebrew first:"
    echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    exit 1
fi

echo "✅ Homebrew is installed"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "📦 Installing Node.js..."
    brew install node
else
    echo "✅ Node.js is installed ($(node --version))"
fi

# Check if pnpm is installed
if ! command -v pnpm &> /dev/null; then
    echo "📦 Installing pnpm..."
    npm install -g pnpm
else
    echo "✅ pnpm is installed ($(pnpm --version))"
fi

# Install PostgreSQL
if ! command -v psql &> /dev/null; then
    echo "📦 Installing PostgreSQL..."
    brew install postgresql@14
    brew services start postgresql@14
else
    echo "✅ PostgreSQL is installed"
    # Start PostgreSQL service
    brew services start postgresql@14
fi

# Create database
echo "🗄️  Setting up database..."
createdb roof_db 2>/dev/null || echo "Database roof_db already exists"

# Set up Python virtual environment
echo "🐍 Setting up Python environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

# Activate virtual environment and install dependencies
echo "📦 Installing Python dependencies..."
source .venv/bin/activate
pip install --upgrade pip
pip install -r backend/requirements-py39.txt

# Set up environment file
echo "⚙️  Setting up environment configuration..."
if [ ! -f "backend/.env" ]; then
    cp backend/env.example backend/.env
    # Update database URL for Mac
    sed -i '' 's/DATABASE_URL=postgresql:\/\/username:password@localhost:5432\/database_name/DATABASE_URL=postgresql:\/\/'$(whoami)'@localhost:5432\/roof_db/' backend/.env
    sed -i '' 's/ELASTIC_URL=https:\/\/localhost:9200/ELASTIC_URL=http:\/\/localhost:9200/' backend/.env
    echo "✅ Environment file created and configured"
else
    echo "✅ Environment file already exists"
fi

# Run database migrations
echo "🔄 Running database migrations..."
alembic upgrade head

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend
pnpm install
cd ..

# Create missing TypeScript config
if [ ! -f "frontend/tsconfig.vitest.json" ]; then
    cat > frontend/tsconfig.vitest.json << 'EOF'
{
  "extends": "./tsconfig.app.json",
  "compilerOptions": {
    "composite": true,
    "lib": [],
    "types": ["node", "jsdom"]
  },
  "include": [
    "src/**/*",
    "src/**/*.vue"
  ]
}
EOF
    echo "✅ Created missing TypeScript config"
fi

# Test builds
echo "🧪 Testing builds..."
echo "Testing backend..."
source .venv/bin/activate
python -c "import sys; sys.path.append('backend'); from app.main import app; print('✅ Backend imports successfully')"

echo "Testing frontend..."
cd frontend
pnpm run build
cd ..

echo ""
echo "🎉 Setup complete! Your Roof project is ready to run on Mac."
echo ""
echo "To start the backend:"
echo "  cd backend && source ../.venv/bin/activate && uvicorn app.main:app --reload"
echo ""
echo "To start the frontend:"
echo "  cd frontend && pnpm run dev"
echo ""
echo "Backend will be available at: http://localhost:8000"
echo "Frontend will be available at: http://localhost:5173"
echo "API docs will be available at: http://localhost:8000/docs"
