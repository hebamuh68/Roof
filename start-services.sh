#!/bin/bash

# Script to start all required services for Roof backend

echo "🚀 Starting Roof Backend Services..."
echo ""

# Check if PostgreSQL is running
echo "📊 Checking PostgreSQL..."
if brew services list | grep -q "postgresql@14.*started"; then
    echo "✅ PostgreSQL is already running"
else
    echo "🔄 Starting PostgreSQL..."
    brew services start postgresql@14
    sleep 2
    echo "✅ PostgreSQL started"
fi

echo ""

# Check if Elasticsearch is running
echo "🔍 Checking Elasticsearch..."
if curl -s http://localhost:9200 > /dev/null 2>&1; then
    echo "✅ Elasticsearch is already running"
else
    echo "🔄 Starting Elasticsearch..."
    export ES_JAVA_HOME=/opt/homebrew/opt/openjdk@17
    /opt/homebrew/opt/elasticsearch-full/bin/elasticsearch > /dev/null 2>&1 &
    echo "⏳ Waiting for Elasticsearch to start..."
    sleep 15

    if curl -s http://localhost:9200 > /dev/null 2>&1; then
        echo "✅ Elasticsearch started successfully"
    else
        echo "❌ Failed to start Elasticsearch"
        exit 1
    fi
fi

echo ""
echo "✨ All services are running!"
echo ""
echo "You can now:"
echo "  1. Start the backend: cd backend && uvicorn app.main:app --reload --port 8000"
echo "  2. Test search: curl 'http://localhost:8000/search/apartments?query=cairo'"
echo ""