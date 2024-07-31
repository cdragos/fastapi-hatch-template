from pydantic_settings import BaseSettings

from pydantic import field_validator


class Settings(BaseSettings):
    """Configuration settings for the application, using environment variables with default values."""

    POSTGRES_DB: str = 'fastapi'
    POSTGRES_PASSWORD: str = 'devpassword'
    POSTGRES_PORT: str = '5432'
    POSTGRES_SERVER: str = 'localhost'
    POSTGRES_USER: str = 'devuser'

    SQLALCHEMY_ASYNC_DATABASE_URI: str = ''

    @field_validator('SQLALCHEMY_ASYNC_DATABASE_URI', mode='after')
    @classmethod
    def assemble_db_connection(cls, v: str | None, info) -> str:
        """Assembles the SQLAlchemy async database URI from individual components if not provided."""
        if v and isinstance(v, str):
            return v

        return f"postgresql+asyncpg://{info.data['POSTGRES_USER']}:{info.data['POSTGRES_PASSWORD']}@{info.data['POSTGRES_SERVER']}/{info.data['POSTGRES_DB']}"


settings = Settings()
