from http import HTTPStatus

import pytest


def get_users_url(app, offset=0, limit=100):
    return f'{app.url_path_for("get_users")}?offset={offset}&limit={limit}'


@pytest.mark.anyio
async def test_get_users(async_app, async_client, async_db, create_user):
    # Create some test users
    users = [
        create_user(first_name='Alice', last_name='Smith', email='alice@example.com'),
        create_user(first_name='Bob', last_name='Jones', email='bob@example.com'),
        create_user(first_name='Charlie', last_name='Brown', email='charlie@example.com'),
    ]
    async_db.add(users[0])
    async_db.add(users[1])
    async_db.add(users[2])

    await async_db.commit()
    await async_db.refresh(users[0])
    await async_db.refresh(users[1])
    await async_db.refresh(users[2])

    # Test default pagination (offset=0, limit=100) and check full user data
    resp = await async_client.get(get_users_url(async_app))
    assert resp.status_code == HTTPStatus.OK
    data = resp.json()
    assert data['count'] == 3
    assert len(data['users']) == 3

    for i, user in enumerate(data['users']):
        assert user['id'] == str(users[i].id)
        assert user['first_name'] == users[i].first_name
        assert user['last_name'] == users[i].last_name
        assert user['email'] == users[i].email

    # Test custom pagination (only check length)
    resp = await async_client.get(get_users_url(async_app, offset=1, limit=2))
    assert resp.status_code == HTTPStatus.OK
    data = resp.json()
    assert data['count'] == 3
    assert len(data['users']) == 2
