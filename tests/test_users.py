def test_create_user_success(client):
    response = client.post(
        "/users",
        json={"name": "Alice", "email": "alice@example.com", "role": "student"},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["name"] == "Alice"


def test_create_user_validation_error(client):
    response = client.post(
        "/users",
        json={"name": "   ", "email": "invalid", "role": "wrong"},
    )

    assert response.status_code == 422


def test_get_all_users_and_user_by_id(client):
    client.post(
        "/users",
        json={"name": "Alice", "email": "alice@example.com", "role": "student"},
    )
    client.post(
        "/users",
        json={"name": "Bob", "email": "bob@example.com", "role": "admin"},
    )

    all_users = client.get("/users")
    assert all_users.status_code == 200
    assert len(all_users.json()) == 2

    user = client.get("/users/2")
    assert user.status_code == 200
    assert user.json()["name"] == "Bob"


def test_get_user_not_found(client):
    response = client.get("/users/999")
    assert response.status_code == 404


def test_create_user_duplicate_email(client):
    client.post(
        "/users",
        json={"name": "Alice", "email": "alice@example.com", "role": "student"},
    )

    response = client.post(
        "/users",
        json={"name": "Alice 2", "email": "alice@example.com", "role": "student"},
    )

    assert response.status_code == 409
