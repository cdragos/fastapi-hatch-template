from fastapi_hatch_template.config import settings
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# Create an async engine using the database URI from settings
engine = create_async_engine(settings.SQLALCHEMY_ASYNC_DATABASE_URI)
# Create an async session factory
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
