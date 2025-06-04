import sys
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.api import api_router
from app.core.config import settings
from app.db.session import engine
from app.db.base_class import Base

# Setup logging
logging.basicConfig(
    stream=sys.stdout, 
    format='%(asctime)-15s %(message)s',
    level=logging.INFO, 
    datefmt=None
)
logger = logging.getLogger("SummarizerMain")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up ...")
    
    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    # Shutdown
    logger.info("Shutting down ...")
    await engine.dispose()


def create_application() -> FastAPI:
    application = FastAPI(
        title="SummarizerAI API",
        description="AI-powered text summarization service",
        version="1.0.0",
        lifespan=lifespan
    )
    
    # Add CORS middleware
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API router
    application.include_router(api_router, prefix="/api/v1")
    
    return application


app = create_application()