def get_token(client):
    client.post("/auth/register", json={
        "username": "taskuser",
        "password": "taskpass"
    })
    response = client.post("/auth/login", json={
        "username": "taskuser",
        "password": "taskpass"
    })
    return response.get_json()["token"]

def test_create_task(client):
    token = get_token(client)
    response = client.post("/tasks/", json={
        "title": "Test Task",
        "description": "A sample task"
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    assert response.get_json()["message"] == "Task created"

def test_get_tasks(client):
    token = get_token(client)
    client.post("/tasks/", json={
        "title": "Task 1"
    }, headers={"Authorization": f"Bearer {token}"})
    response = client.get("/tasks/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.get_json()
    assert "tasks" in data
    assert isinstance(data["tasks"], list)
    assert len(data["tasks"]) >= 1

def test_update_task(client):
    token = get_token(client)
    client.post("/tasks/", json={
        "title": "Old Task"
    }, headers={"Authorization": f"Bearer {token}"})
    task_id = 1
    response = client.put(f"/tasks/{task_id}", json={
        "title": "Updated Task"
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.get_json()["message"] == "Task updated"

def test_delete_task(client):
    token = get_token(client)
    client.post("/tasks/", json={
        "title": "Task to Delete"
    }, headers={"Authorization": f"Bearer {token}"})
    response = client.delete("/tasks/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.get_json()["message"] == "Task deleted"

def test_get_tasks_pagination_and_filtering(client):
    token = get_token(client)

    tasks_data = [
        {"title": "Task 1", "completed": True},
        {"title": "Task 2", "completed": False},
        {"title": "Task 3", "completed": True},
        {"title": "Task 4", "completed": False},
        {"title": "Task 5", "completed": True},
    ]
    for task in tasks_data:
        client.post("/tasks/", json={"title": task["title"]}, headers={"Authorization": f"Bearer {token}"})

    resp = client.get("/tasks/?completed=true&per_page=2", headers={"Authorization": f"Bearer {token}"})
    data = resp.get_json()
    assert resp.status_code == 200
    for t in data["tasks"]:
        assert "completed" in t

    assert len(data["tasks"]) <= 2
    assert data["page"] == 1
    assert data["per_page"] == 2

    resp = client.get("/tasks?completed=false", headers={"Authorization": f"Bearer {token}"})
    data = resp.get_json()
    assert resp.status_code == 200
    for t in data["tasks"]:
        assert "completed" in t

    resp = client.get("/tasks?page=2&per_page=2", headers={"Authorization": f"Bearer {token}"})
    data = resp.get_json()
    assert resp.status_code == 200
    assert data["page"] == 2
    assert data["per_page"] == 2

    resp = client.get("/tasks?completed=maybe", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 400
    assert "error" in resp.get_json()
