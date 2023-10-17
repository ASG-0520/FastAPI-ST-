from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# DATA BASE:
def test_user_show_fake_base():
    response = client.get("/user/", headers={"X-token": "fake-super-secret-token"})
    assert response.status_code == 200


def test_show_fake_base_bad_token():
    response = client.get("/user/", headers={"X-Token": "hailhydra"})
    assert response.status_code == 400
    assert response.json() == {"detail": "X-Token header invalid"}


# USERS:

# Get User
def test_get_user():
    response = client.get("/user/1", headers={"X-token": "fake-super-secret-token"})
    assert response.status_code == 200
    assert response.json() == {
        "User ID": 1,
        "UserName": "Chuck Norris"
    }


def test_get_user_bad_token():
    response = client.get("user//1", headers={"X-token": "camasutra"})
    assert response.status_code == 400
    assert response.json() == {"detail": "X-Token header invalid"}


# non_existent_user
def test_get_non_existent_user():
    response = client.get("/user/10", headers={"X-token": "fake-super-secret-token"})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found."}
