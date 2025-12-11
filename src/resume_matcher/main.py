import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .api.v1.router import api_router

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""

    app = FastAPI(
        title=settings.app_name,
        description="""
        Resume Matcher API - Match resumes to job descriptions using AI embeddings.

        ## Features

        * **Upload resumes** - PDF parsing and text extraction
        * **Add job postings** - Store job descriptions
        * **Semantic matching** - Find best matches using vector similarity

        ## How it works

        1. Upload a resume (PDF)
        2. Add job descriptions
        3. Get ranked matches based on semantic similarity
        """,
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure properly for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(api_router, prefix=settings.api_v1_prefix)

    # Health check endpoint
    @app.get("/health")
    def health_check():
        return {"status": "healthy", "version": "0.1.0"}

    @app.get("/")
    def root():
        return {
            "message": "Welcome to Resume Matcher API",
            "docs": "/docs",
            "health": "/health",
        }

    logger.info(f"Application created: {settings.app_name}")

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "resume_matcher.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
    )