import asyncio
from contextlib import asynccontextmanager

import typer
from fastapi_hatch_template.db.session import AsyncSessionLocal
from scripts import seed_data

app = typer.Typer()


@asynccontextmanager
async def get_db():
    """
    Provide a transactional scope around a series of operations.

    Yields an AsyncSession for database operations and ensures it is closed after use.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def async_seed_db():
    """Asynchronously seed the database using the seed_data function."""
    async with get_db() as db:
        await seed_data(db)
    print('Database seeded successfully!')


@app.command()
def seed_db():
    """Command to run the async_seed_db function synchronously."""
    asyncio.run(async_seed_db())


@app.command()
def hello():
    print('Hello World')


if __name__ == '__main__':
    app()
