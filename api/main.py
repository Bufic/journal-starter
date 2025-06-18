import logging
import asyncio
from fastapi import FastAPI
from dotenv import load_dotenv
from api.controllers import journal_router
from .init_db import init_db

load_dotenv()

# TODO: Setup basic console logging
# Hint: Use logging.basicConfig() with level=logging.INFO

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
logger.info("Starting Journal API...")

app = FastAPI()

# Run init_db when app starts


@app.on_event("startup")
async def startup_event():
    logger.info("Initializing database...")
    await init_db()
    logger.info("Database initialized.")

app.include_router(journal_router)
logger.info("Journal API started successfully.")
