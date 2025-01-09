from pydantic_settings import BaseSettings
from pydantic import ValidationError


class Settings(BaseSettings):
    # Database configuration
    SQLALCHEMY_DATABASE_URL: str

    # JWT configuration
    JWT_SECRET: str
    JWT_EXPIRATION: int
    ALGORITHM: str = "HS256"

    # Redis configuration
    REDIS_HOST: str
    REDIS_PORT: int

    class Config:
        env_file = ".env"


try:
    settings = Settings()
except ValidationError as e:
    raise RuntimeError(f"Configuration error: {e}")
