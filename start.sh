#!/bin/bash
set -e

# Navigate to the backend directory
cd "$(dirname "$0")"

# Run database migrations
echo "Running database migrations..."
alembic upgrade head

# Start the FastAPI server
echo "Starting Expense Tracker Backend..."
# Use the PORT environment variable if available (Render provides this)
PORT=${PORT:-10000}
uvicorn app.main:app --host 0.0.0.0 --port $PORT
