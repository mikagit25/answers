from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
from core.config import settings

app = FastAPI(title="Answers API", version="1.0.0")

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
    return {"status": "ok", "timestamp": time.time()}

# Include API routers
from api.routes import ask, compare

app.include_router(ask.router, prefix="/api/v1/ask", tags=["Ask"])
app.include_router(compare.router, prefix="/api/v1/compare", tags=["Compare"])
