def setup_ticket(client):
    client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "123456"
    })

    login = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "123456"
    })

    token = login.get_json()["data"]["access_token"]

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

    client.post(
        "/tickets/buy",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "flight_number": "TK101",
            "date": "2026-04-01T09:00:00",
            "passenger_names": ["Ilayda Gun"]
        }
    )


def test_checkin(client):
    setup_ticket(client)

    response = client.post("/checkin/", json={
        "flight_number": "TK101",
        "date": "2026-04-01T09:00:00",
        "passenger_name": "Ilayda Gun"
    })

    assert response.status_code == 200