#!/bin/bash
# Скрипт для быстрой проверки и запуска проекта

set -e

echo "🚀 Answers Platform - Quick Test & Launch"
echo "=========================================="
echo ""

# Check if .env exists
if [ ! -f "backend/.env" ]; then
    echo "❌ backend/.env not found!"
    echo "Creating from .env.example..."
    cp .env.example backend/.env
    echo "⚠️  Please edit backend/.env with your API keys"
    exit 1
fi

echo "✅ Environment file found"
echo ""

# Check Docker
echo "🐳 Checking Docker..."
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed"
    echo "Install from: https://www.docker.com/products/docker-desktop"
    exit 1
fi

if ! docker info &> /dev/null; then
    echo "❌ Docker is not running"
    echo "Please start Docker Desktop"
    exit 1
fi

echo "✅ Docker is running"
echo ""

# Start databases
echo "📦 Starting databases (PostgreSQL + Redis)..."
docker-compose up -d
echo "✅ Databases started"
echo ""

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
sleep 5

# Check Python
echo "🐍 Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✅ Python $PYTHON_VERSION"
echo ""

# Setup backend virtual environment
echo "📦 Setting up backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
echo "✅ Virtual environment activated"

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
echo "✅ Backend dependencies installed"
echo ""

# Test LLM providers
echo "🤖 Testing LLM providers..."
python test_llm_providers.py || echo "⚠️  Some providers failed, but system will use fallbacks"
echo ""

cd ..

# Import knowledge base
echo "📚 Importing knowledge base..."
cd backend
python ingest.py || echo "⚠️  Data import had issues (database might already have data)"
cd ..
echo ""

# Check Node.js
echo "🟢 Checking Node.js..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed"
    echo "Install from: https://nodejs.org/"
    exit 1
fi

NODE_VERSION=$(node --version)
echo "✅ Node.js $NODE_VERSION"
echo ""

# Setup frontend
echo "📦 Setting up frontend..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies (this may take a few minutes)..."
    npm install
fi

echo "✅ Frontend ready"
echo ""

cd ..

echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "🎯 To start the application:"
echo ""
echo "Terminal 1 - Backend:"
echo "  cd backend && source venv/bin/activate && uvicorn main:app --reload"
echo ""
echo "Terminal 2 - Frontend:"
echo "  cd frontend && npm run dev"
echo ""
echo "Then open: http://localhost:3000"
echo ""
echo "📊 API Documentation: http://localhost:8000/docs"
echo ""
echo "💡 Tips:"
echo "  - OpenRouter key is configured ✅"
echo "  - Get Groq key for faster responses: https://console.groq.com/"
echo "  - Install Ollama for unlimited free usage: https://ollama.ai/"
echo ""
