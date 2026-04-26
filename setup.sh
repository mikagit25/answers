#!/bin/bash
# Setup script for Answers platform

set -e

echo "🚀 Setting up Answers Platform..."

# Check if Python 3.11+ is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✓ Python version: $PYTHON_VERSION"

# Setup backend
echo ""
echo "📦 Setting up backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing backend dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Copy .env.example to .env
if [ ! -f ".env" ]; then
    echo "Creating .env file from .env.example..."
    cp ../.env.example .env
    echo "⚠️  Please edit backend/.env with your configuration"
fi

cd ..

# Setup frontend
echo ""
echo "📦 Setting up frontend..."
cd frontend

# Install dependencies
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit backend/.env with your database and API credentials"
echo "2. Start databases: docker-compose up -d"
echo "3. Import knowledge base: cd backend && python ingest.py"
echo "4. Start backend: cd backend && uvicorn main:app --reload"
echo "5. Start frontend: cd frontend && npm run dev"
echo ""
echo "Open http://localhost:3000 in your browser"
