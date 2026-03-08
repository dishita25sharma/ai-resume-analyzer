"""
AI Resume Analyzer - FastAPI Backend
Main application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.resume_routes import router as resume_router
from utils.logger import get_logger

logger = get_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Resume Analyzer",
    description="Backend API for resume analysis using LLM",
    version="0.1.0"
)

logger.info("FastAPI application initialized")

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("CORS middleware configured")

# Include resume routes
app.include_router(resume_router, prefix="/api", tags=["resume"])

logger.info("Resume routes registered")


@app.get("/")
async def root():
    """
    Root endpoint to verify the API is running
    """
    return {
        "message": "Welcome to AI Resume Analyzer API",
        "version": "0.1.0",
        "endpoints": {
            "upload_resume": "POST /api/upload-resume",
            "health": "GET /"
        }
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    logger.info("Health check performed")
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting AI Resume Analyzer API Server")
    uvicorn.run(app, host="0.0.0.0", port=8000)
