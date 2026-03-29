def get_token(client):
    client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "123456"
    })

    res = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "123456"
    })

    return res.get_json()["data"]["access_token"]


def test_add_flight_success(client):
    token = get_token(client)

    response = client.post(
        "/flights/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "flight_number": "TK101",
            "date_from": "2026-04-01T09:00:00",
            "date_to": "2026-04-01T11:00:00",
            "airport_from": "Izmir",
            "airport_to": "Istanbul",
            "duration": 120,
            "capacity": 50
        }
    )

    assert response.status_code == 201


def test_query_flight(client):
    token = get_token(client)

    client.post(
        "/flights/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "flight_number": "TK101",
            "date_from": "2026-04-01T09:00:00",
            "date_to": "2026-04-01T11:00:00",
            "airport_from": "Izmir",
            "airport_to": "Istanbul",
            "duration": 120,
            "capacity": 50
        }
    )

    response = client.get("/flights/query?airport_from=Izmir&airport_to=Istanbul")

    assert response.status_code == 200