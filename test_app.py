import os
import tempfile
import pytest
from app import app, init_db

@pytest.fixture()
def client():
    fd, path = tempfile.mkstemp()
    os.close(fd)
    app.config["TESTING"] = True
    global_module = __import__("app")
    global_module.DATABASE = path
    init_db()
    with app.test_client() as client:
        yield client
    os.unlink(path)

def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Available Vehicles" in response.data

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "ok"

def test_vehicle_api(client):
    response = client.get("/api/vehicles")
    assert response.status_code == 200
    assert len(response.json) >= 1
