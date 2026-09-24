from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_seeded_records_and_relationship_validation():
    assert client.get("/customers").status_code == 200
    assert len(client.get("/customers").json()) == 3
    assert len(client.get("/devices").json()) == 3
    assert len(client.get("/repairs").json()) == 3

    invalid_device = client.post(
        "/devices",
        json={"customer_id": 999, "device_type": "Laptop", "brand": "Dell", "model": "X"},
    )
    assert invalid_device.status_code == 404

    invalid_repair = client.post(
        "/repairs",
        json={"device_id": 999, "problem": "Broken", "repair_cost": 100, "repair_status": "Pending"},
    )
    assert invalid_repair.status_code == 404

    negative_cost = client.post(
        "/repairs",
        json={"device_id": 1, "problem": "Broken", "repair_cost": -1, "repair_status": "Pending"},
    )
    assert negative_cost.status_code == 422


def test_repair_status_workflow():
    for repair_status in ("In Progress", "Completed", "Delivered"):
        response = client.put("/repairs/1/status", json={"repair_status": repair_status})
        assert response.status_code == 200
        assert response.json()["repair_status"] == repair_status
