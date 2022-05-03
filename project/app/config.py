import os
import sys
from functools import lru_cache

from pydantic import AnyUrl, BaseSettings

import logging
logging.basicConfig(stream=sys.stdout, format='%(asctime)-15s %(message)s',
                level=logging.INFO, datefmt=None)
logger = logging.getLogger("Summarizer")


class Settings(BaseSettings):
    environment: str = os.getenv("ENVIRONMENT", "dev")
    testing: bool = os.getenv("TESTING", 0)
    database_url: AnyUrl = os.getenv("DATABASE_URL")
    hf_token: str = os.getenv("HF_TOKEN")


# lru_cache: save the setting values in memory avoiding to re-download they for each request.
@lru_cache
def get_settings() -> BaseSettings:
    logger.info("Loading config settings from the environment ...")
    return Settings()

