# 📘 Answers Platform - Quick Start Guide

## Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Git

## Installation

### Option 1: Automated Setup (Recommended)
```bash
./setup.sh
```

### Option 2: Manual Setup

#### 1. Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example .env
```

Edit `backend/.env` with your credentials:
```bash
DATABASE_URL=postgresql://user:password@localhost:5432/answers_db
REDIS_URL=redis://localhost:6379
QWEN_API_KEY=your_qwen_api_key_here
```

#### 2. Frontend Setup
```bash
cd frontend
npm install
```

#### 3. Database Setup
```bash
# Start PostgreSQL and Redis
docker-compose up -d

# Import knowledge base
cd backend
python ingest.py
```

## Running the Application

### Development Mode

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Production Build

**Backend:**
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm run build
npm start
```

## Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

## API Documentation

Once the backend is running, visit:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Project Structure

```
answers/
├── backend/                 # FastAPI backend
│   ├── api/                # API routes and schemas
│   ├── core/               # Configuration and security
│   ├── db/                 # Database models and connection
│   ├── rag/                # RAG pipeline (prompts, validator)
│   ├── tests/              # Pytest tests
│   ├── ingest.py           # Data import script
│   └── main.py             # Application entry point
├── frontend/               # Next.js + PWA frontend
│   ├── app/                # Next.js App Router pages
│   ├── components/         # React components
│   ├── lib/                # API client and utilities
│   └── public/             # Static assets and PWA files
├── knowledge_base/         # JSON data sources
├── docker-compose.yml      # Docker services
└── setup.sh                # Automated setup script
```

## Common Issues

### Database Connection Error
Make sure Docker containers are running:
```bash
docker-compose ps
```

### Module Not Found (Python)
Activate virtual environment:
```bash
cd backend
source venv/bin/activate
```

### Port Already in Use
Change ports in `docker-compose.yml` or stop conflicting services.

## Deployment

### Frontend (Vercel)
```bash
cd frontend
vercel deploy
```

### Backend (Render/Railway)
Connect your GitHub repository and configure environment variables.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

MIT License - See LICENSE file for details
