import time
from datetime import datetime, timedelta

import requests
from constants import (
    HEADERS, PARKKI_HOST, PARKKI_HTTP_HOST, TEST_DOMAIN,
    TEST_PAYMENT_ZONE_NUMBER, TIMEFORMAT)
from utils import value_in_list_of_dicts

NOW = datetime.now()

DATA = {
    "zone": TEST_PAYMENT_ZONE_NUMBER,
    "domain": TEST_DOMAIN,
    "location": {
        "type": "Point",
        "coordinates": [
            22.2621559,
            60.4525144
        ]
    },
    "registration_number": "TES-7",
}


def test_get_payment_zones():
    response = requests.get(f"{PARKKI_HOST}/operator/v1/payment_zone/", headers=HEADERS)
    assert response.status_code == 200
    json_data = response.json()
    assert "count" in json_data
    assert "results" in json_data
    assert "next" in json_data
    assert "previous" in json_data
    assert json_data["count"] > 0
    assert value_in_list_of_dicts(TEST_DOMAIN, json_data["results"]) is True
    assert value_in_list_of_dicts("1", json_data["results"]) is True
    assert "name" in json_data["results"][0]
    assert "code" in json_data["results"][0]
    assert "domain" in json_data["results"][0]


def test_get_permit_areas():
    response = requests.get(f"{PARKKI_HOST}/operator/v1/permit_area/", headers=HEADERS)
    assert response.status_code == 200
    json_data = response.json()
    assert "count" in json_data
    assert "results" in json_data
    assert json_data["count"] > 0
    assert "name" in json_data["results"][0]
    assert "code" in json_data["results"][0]
    assert "domain" in json_data["results"][0]
    assert value_in_list_of_dicts(TEST_DOMAIN, json_data["results"]) is True
    assert value_in_list_of_dicts("A", json_data["results"]) is True


def test_create_not_valid_parking_to_http(data=DATA):
    # Fails as posting to HTTP and not HTTPS
    response = requests.post(f"{PARKKI_HTTP_HOST}/operator/v1/parking/", headers=HEADERS, json=data)
    assert response.status_code == 405
    assert "not allowed" in response.text


def test_create_not_valid_parking(data=DATA):
    # 'time_start' and 'time_end in the past
    data["time_start"] = (NOW - timedelta(hours=5)).strftime(TIMEFORMAT)
    data["time_end"] = (NOW - timedelta(hours=4)).strftime(TIMEFORMAT)
    response = requests.post(f"{PARKKI_HOST}/operator/v1/parking/", headers=HEADERS, json=data)
    assert response.status_code == 201
    json_data = response.json()
    assert json_data["status"] == "not_valid"
    assert json_data["domain"] == TEST_DOMAIN
    assert json_data["registration_number"] == data["registration_number"]
    return json_data["id"]


def test_create_valid_parking(data=DATA):
    data["time_start"] = (NOW - timedelta(hours=4)).strftime(TIMEFORMAT)
    data["time_end"] = (NOW + timedelta(days=1, hours=1)).strftime(TIMEFORMAT)
    response = requests.post(f"{PARKKI_HOST}/operator/v1/parking/", headers=HEADERS, json=data)
    assert response.status_code == 201
    json_data = response.json()
    assert json_data["status"] == "valid"
    assert json_data["domain"] == TEST_DOMAIN
    assert json_data["registration_number"] == data["registration_number"]
    return json_data["id"]


def test_delete_parking(id):
    response = requests.delete(f"{PARKKI_HOST}/operator/v1/parking/{id}/", headers=HEADERS)
    assert response.status_code == 204


def test_parking_replace_by_id_and_grace_period(id, data=DATA):
    data["registration_number"] = "TES-8"
    response = requests.patch(f"{PARKKI_HOST}/operator/v1/parking/{id}/", headers=HEADERS, json=data)
    json_data = response.json()
    assert json_data["status"] == "valid"
    assert json_data["domain"] == TEST_DOMAIN
    assert json_data["registration_number"] == "TES-8"
    print("Waiting for 130seconds, to test that grace period(2 minutes) has passed....")
    data["registration_number"] = "TES-8"
    time.sleep(130)
    response = requests.put(f"{PARKKI_HOST}/operator/v1/parking/{id}/", headers=HEADERS, json=data)
    response.status_code == 403
    assert "Grace period has passed" in response.json()["detail"]


if __name__ == "__main__":
    test_get_payment_zones()
    test_get_permit_areas()
    test_create_not_valid_parking_to_http(DATA)
    id = test_create_not_valid_parking(DATA)
    test_delete_parking(id)
    id = test_create_valid_parking()
    test_parking_replace_by_id_and_grace_period(id)
    test_delete_parking(id)
