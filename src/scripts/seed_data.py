import csv
from pathlib import Path
from typing import Any

import aiofiles
from models.user import User

from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

PROJECT_ROOT = Path(__file__).parent.parent.parent

_CSV_CONFIG = [
    {'file': PROJECT_ROOT / 'seeds' / 'users.csv', 'model': User, 'index_elements': ['email']},
    # Add more CSV files and models as needed
    # Example: {"file": PROJECT_ROOT / "seeds" / "products.csv", "model": Product, "index_elements": ['product_code']}
]


async def seed_data(db: AsyncSession) -> None:
    """
    Seed data from multiple CSV files into their corresponding database tables.

    :param db: AsyncSession for database operations
    """
    for config in _CSV_CONFIG:
        data = await load_data_from_csv(config['file'])
        await insert_data(db, config['model'], data, config['index_elements'])


def parse_csv_value(key: str, value: str) -> Any:
    """
    Parse a single value from CSV, applying appropriate type conversions.

    :param key: The column name
    :param value: The value to parse
    :return: Parsed value
    """
    # Convert boolean strings
    if value.lower() in ['true', 'false']:
        return value.lower() == 'true'

    # Convert numeric strings
    if value.isdigit():
        return int(value)

    return value


async def load_data_from_csv(file_path: Path) -> list[dict[str, Any]]:
    """
    Load and parse data from a CSV file asynchronously.

    :param file_path: Path to the CSV file
    :return: List of dictionaries representing the parsed data
    """
    async with aiofiles.open(file_path) as csvfile:
        content = await csvfile.read()
        csvreader = csv.DictReader(content.splitlines())

        parsed_data = []
        for row in csvreader:
            parsed_row = {}
            for key, value in row.items():
                parsed_row[key] = parse_csv_value(key, value)
            parsed_data.append(parsed_row)

        return parsed_data


async def insert_data(
    db: AsyncSession, model: type[Any], data: list[dict[str, Any]], index_elements: list[str]
) -> None:
    """
    Insert data into the database table corresponding to the model, handling conflicts by doing nothing.

    :param db: AsyncSession for database operations
    :param model: SQLAlchemy model representing the target table
    :param data: List of dictionaries representing the data to be inserted
    :param index_elements: List of column names to identify unique rows for conflict handling
    """
    stmt = pg_insert(model).values(data)
    stmt = stmt.on_conflict_do_nothing(index_elements=index_elements)
    result = await db.execute(stmt)
    await db.commit()
    print(f'Seeding complete for {model.__name__}. {result.rowcount} new records added.')
