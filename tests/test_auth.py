def test_register_success(client):
    response = client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "123456"
    })

    assert response.status_code == 201


def test_login_success(client):
    client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "123456"
    })

    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "123456"
    })

    data = response.get_json()

    assert response.status_code == 200
    assert "access_token" in data["data"]