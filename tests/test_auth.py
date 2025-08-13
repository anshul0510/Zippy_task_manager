def test_register(client):
    response = client.post("/auth/register", json={
        "username": "testuser",
        "password": "testpass"
    })
    assert response.status_code == 201
    assert response.get_json()["message"] == "User registered successfully"

def test_login(client):
    # Register first
    client.post("/auth/register", json={
        "username": "testuser",
        "password": "testpass"
    })

    # Login
    response = client.post("/auth/login", json={
        "username": "testuser",
        "password": "testpass"
    })
    assert response.status_code == 200
    assert "token" in response.get_json()
