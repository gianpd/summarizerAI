import sys
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import ping, summaries
from app.db import init_db

logging.basicConfig(stream=sys.stdout, format='%(asctime)-15s %(message)s',
                level=logging.INFO, datefmt=None)
logger = logging.getLogger("SummarizerMain")


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(ping.router)
    application.include_router(
        summaries.router, prefix="/summaries", tags=["summaries"]
    )
    return application


app = create_application()

origins = [
    'http://localhost:3000' # testing the frontend
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up ...")
    init_db(app)


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down ...")
