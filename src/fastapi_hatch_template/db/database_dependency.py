from collections.abc import AsyncGenerator

from .session import AsyncSessionLocal


async def get_async_db() -> AsyncGenerator:
    """
    Provides an asynchronous database session generator.

    This function yields an AsyncSession for database operations and ensures
    the session is committed after use.
    """
    async with AsyncSessionLocal() as session:
        yield session
        await session.commit()
