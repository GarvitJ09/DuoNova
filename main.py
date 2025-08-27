import sys
import os

# Add the current directory to Python path to ensure imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.resume import router as resume_router
from app.api.runtime_config import router as runtime_config_router
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create FastAPI application
app = FastAPI(
    title="ATS-Checker API",
    description="Advanced resume processing and analysis system with multi-LLM support",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(resume_router, prefix="/api/v1", tags=["Resume Processing"])
app.include_router(runtime_config_router, prefix="/api/v1", tags=["Configuration Management"])

@app.get("/")
async def root():
    """Root endpoint providing API information."""
    return {
        "message": "ATS-Checker API",
        "version": "1.0.0",
        "docs": "/docs",
        "features": [
            "Multi-format resume processing (PDF, DOCX)",
            "Hybrid extraction (Library + LLM)",
            "Multi-LLM provider support (OpenAI, Groq)",
            "Automatic fallback system",
            "MongoDB cloud storage",
            "Comprehensive data validation"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "ats-checker-api"}

if __name__ == "__main__":
    # Get configuration from environment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info"
    )
