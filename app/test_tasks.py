from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# Create task
def test_post_task():
    response = client.post("/task/1",
                           headers={"X-token": "fake-super-secret-token"},
                           json={"name": "1", "description": "one", "detail": "1", "status": True})
    assert response.status_code == 200
    assert response.json() == {"name": "1", "description": "one", "detail": "1", "status": True}


# Create Existing Task
def test_create_existing_task():
    response = client.post("/task/1",
                           headers={"X-token": "fake-super-secret-token"},
                           json={"name": "one", "description": "1", "detail": "1", "status": True})
    assert response.status_code == 400
    assert response.json() == {"detail": "This ID already exist"}


# Get Task
def test_get_task_via_id():
    response = client.get("/task/1",
                          headers={"X-token": "fake-super-secret-token"})
    assert response.status_code == 200
    assert response.json() == {
        "name": "1",
        "description": "one",
        "detail": "1",
        "status": True
    }
