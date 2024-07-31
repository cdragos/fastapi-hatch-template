from models import User

import pytest


@pytest.fixture
def create_user(async_db):
    def _create_user(
        email,
        first_name=None,
        last_name=None,
        hashed_password='hashed_password',
        is_active=True,
    ):
        """A callable fixture to create a User object in the database."""
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            hashed_password=hashed_password,
            is_active=is_active,
        )
        return user

    return _create_user
