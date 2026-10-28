import importlib
import os

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("DB_PATH", str(tmp_path / "t.db"))
    monkeypatch.setenv("APP_PASSWORD", "pw")
    monkeypatch.setenv("SECRET_KEY", "k")
    monkeypatch.setenv("COOKIE_SECURE", "0")
    import app.main as main
    importlib.reload(main)
    return TestClient(main.app, follow_redirects=False)


def login(c):
    assert c.post("/login", data={"password": "pw"}).status_code == 303


def test_requires_login(client):
    assert client.get("/").headers["location"] == "/login"
    assert client.post("/clients", data={"name": "x"}).headers["location"] == "/login"


def test_bad_password(client):
    assert "Wrong password" in client.post("/login", data={"password": "no"}).text


def test_full_flow(client):
    login(client)
    r = client.post("/clients", data={"name": "Acme"})
    cid = r.headers["location"].split("/")[-1]
    r = client.post(f"/clients/{cid}/projects", data={"name": "Site", "status": "blocked"})
    pid = r.headers["location"].split("/")[-1]
    client.post(f"/projects/{pid}/tasks", data={"title": "Old", "due_date": "2000-01-01"})
    dash = client.get("/").text
    assert "Old" in dash and "Site" in dash
    client.post("/tasks/1/toggle")
    assert "Old" not in client.get("/").text.split("Overdue tasks")[1].split("Blocked")[0]
    client.post(f"/clients/{cid}/delete")
    assert "Acme" not in client.get("/clients").text
    assert client.get(f"/projects/{pid}").headers["location"] == "/"
