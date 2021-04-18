import json
from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

raw_data = (
    '{"measurement": [{"value": 33.375,"place": "inbox","type": "T"},'
    '{"value": 22.25,"place": "bureau","type": "T"},{"value": 6.875,"place":'
    ' "dehors","type": "T"},{"value": 42.8,"place": "capi2_CPU","type": "T"}],'
    '"time": "07.03.2021 10:00:26"}'
)

raw_data2 = (
    '{"time": "07.03.2021   10:00:49", "measurement":'
    '[{"type": "T", "place": "k\\u00f6niz_bureau", "value": 22.812},'
    ' {"type": "T", "place": "capi4_CPU", "value": 40.4}]}'
)


def test_post_records():
    d = json.loads(raw_data)
    headers = {"X-Secret-Key": "1234"}
    response = client.post("/record", json=d, headers=headers)
    assert response.status_code == 200


def test_post_records2():
    d = json.loads(raw_data2)
    headers = {"X-Secret-Key": "1234"}
    response = client.post("/record", json=d, headers=headers)
    assert response.status_code == 200


def test_get_record():
    response = client.get("/record/1")
    assert response.status_code == 200


def test_get_measurements():
    response = client.get("/measurement")
    assert response.status_code == 200


def test_get_measurement():
    response = client.get("/measurement/1")
    assert response.status_code == 200
