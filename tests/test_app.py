from fastapi.testclient import TestClient

from server.main import app

client = TestClient(app)


def test_read_root() -> None:
    response = client.post("/users", json={
        'name': 'Alex Noname'
    })
    assert response.status_code == 200
    assert response.json() == {"is_ok": False}
