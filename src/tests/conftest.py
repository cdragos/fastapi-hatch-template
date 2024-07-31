from fastapi_hatch_template.config import settings
from fastapi_hatch_template.db.database_dependency import get_async_db
from models import Base

import pytest
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from testcontainers.postgres import PostgresContainer

from .factories import *  # noqa


@pytest.fixture(scope='session')
def anyio_backend():
    """Specify the backend to be used by anyio."""
    return 'asyncio'


@pytest.fixture
def async_app(async_db):
    """Provides the FastAPI app with an overridden dependency to use the async database session."""
    from fastapi_hatch_template.main import app

    async def override_get_async_db():
        yield async_db

    app.dependency_overrides[get_async_db] = override_get_async_db

    return app


@pytest.fixture
async def async_client(async_app):
    """Creates a new instance of an async client for the application."""
    async with AsyncClient(app=async_app, base_url='http://test') as async_client:
        yield async_client


@pytest.fixture(scope='session')
def test_postgres():
    """Starts and stops the Postgres test container."""
    test_postgres = PostgresContainer('postgres:9.5')
    test_postgres.start()
    yield test_postgres
    test_postgres.stop()


@pytest.fixture
async def async_db(test_postgres, monkeypatch):
    """
    Asynchronously establishes a connection with the test database, creates tables,
    yields the session and rolls back any changes.
    """
    test_postgres.driver = '+asyncpg'
    postgres_async_url = test_postgres.get_connection_url()

    monkeypatch.setattr(settings, 'SQLALCHEMY_ASYNC_DATABASE_URI', postgres_async_url)

    async_engine = create_async_engine(postgres_async_url)
    async_session = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

    async with async_engine.begin() as connection:
        await connection.execute(text('CREATE EXTENSION IF NOT EXISTS pgcrypto'))
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
        async with async_session(bind=connection) as session:
            yield session
            await session.flush()
            await session.rollback()
