from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/summarizerdb"
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    environment: str = "development"
    debug: bool = True
    
    # CORS settings
    allowed_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:12000",
        "http://localhost:12001",
        "https://work-1-nddcgiroczfpnzeg.prod-runtime.all-hands.dev",
        "https://work-2-nddcgiroczfpnzeg.prod-runtime.all-hands.dev"
    ]
    
    # External APIs
    hf_token: str = ""
    
    class Config:
        env_file = ".env"


settings = Settings()