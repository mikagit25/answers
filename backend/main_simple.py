"""
Упрощенная версия main.py для запуска без Docker/PostgreSQL.
Использует SQLite для тестирования и разработки.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from core.config import settings

app = FastAPI(title="Answers API (SQLite Mode)", version="1.0.0")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "timestamp": time.time(),
        "database": "sqlite",
        "mode": "development"
    }

# Include simplified API routers
try:
    from api.routes import ask_simple as ask, compare, providers
    
    app.include_router(ask.router, prefix="/api/v1/ask", tags=["Ask"])
    app.include_router(compare.router, prefix="/api/v1/compare", tags=["Compare"])
    app.include_router(providers.router, prefix="/api/v1/providers", tags=["Providers"])
    
    print("✅ All routes loaded successfully")
except Exception as e:
    print(f"⚠️  Warning: Some routes failed to load: {e}")
    import traceback
    traceback.print_exc()

if __name__ == "__main__":
    import uvicorn
    print("\n🚀 Starting Answers API (SQLite mode)...")
    print("📍 API Docs: http://localhost:8000/docs")
    print("💾 Database: SQLite (answers.db)")
    print("🤖 LLM Provider: Groq (with fallback)\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
