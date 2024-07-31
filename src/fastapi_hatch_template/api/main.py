from models import User

from fastapi import APIRouter, Depends, Query
from fastapi_hatch_template.db.database_dependency import get_async_db
from fastapi_hatch_template.schemas import UserSchema, UsersResponseSchema
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get('/users', response_model=UsersResponseSchema)
async def get_users(
    offset: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000), db: AsyncSession = Depends(get_async_db)
):
    """
    Retrieve a paginated list of users.

    Args:
        offset (int): Number of users to skip (for pagination).
        limit (int): Maximum number of users to return.
        db (AsyncSession): Injected database session.

    Returns:
        UsersResponseSchema: Paginated list of users.
    """

    count_statement = select(func.count()).select_from(User)
    count = (await db.execute(count_statement)).scalar() or 0

    query = select(User).offset(offset).limit(limit)
    result = await db.execute(query)
    # Convert SQLAlchemy models to Pydantic schemas
    users = [UserSchema.model_validate(user) for user in result.scalars().all()]

    # Return paginated user list wrapped in response schema
    return UsersResponseSchema(users=users, count=count)
