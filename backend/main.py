"""
RESEARCHMINDAI - Main Server Entrypoint
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import logging

from config import settings
from database import init_db
from api.routes.research import router as research_router
from api.routes.documents import router as documents_router
from api.routes.reports import router as reports_router
from api.routes.features import router as features_router

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    logger.info("Initializing ResearchMind AI services...")
    settings.ensure_dirs()
    await init_db()
    logger.info("Database tables initialized. Server ready.")
    yield
    # Shutdown actions
    logger.info("Shutting down ResearchMind AI services...")

app = FastAPI(
    title="ResearchMind AI",
    description="Multi-agent search, fact-checking, RAG synthesis, and automated document generation.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static directories for uploads and reports downloading
settings.ensure_dirs()
app.mount("/static/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")
app.mount("/static/reports", StaticFiles(directory=settings.reports_dir), name="reports")

# Register API Routers
app.include_router(research_router, prefix="/api/research", tags=["Research"])
app.include_router(documents_router, prefix="/api/documents", tags=["Documents"])
app.include_router(reports_router, prefix="/api/reports", tags=["Reports"])
app.include_router(features_router, prefix="/api/features", tags=["Features"])

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "online",
        "settings": {
            "default_llm": settings.default_llm,
            "max_research_depth": settings.max_research_depth
        }
    }

@app.get("/")
async def root():
    return {
        "message": "Welcome to ResearchMind AI API. Navigate to /docs for Swagger documentation."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.backend_host, port=settings.backend_port, reload=True)
