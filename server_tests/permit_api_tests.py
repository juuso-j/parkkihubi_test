from copy import deepcopy
from datetime import datetime, timedelta

import requests
from constants import (
    HEADERS, PARKKI_HOST, TEST_DOMAIN, TEST_EXTERNAL_ID,
    TEST_PERMIT_AREA_IDENTIFIER_1, TEST_PERMIT_SERIES_ID, TIMEFORMAT)
from utils import value_in_list_of_dicts

NOW = datetime.now()
DATA = {
    "series": TEST_PERMIT_SERIES_ID,
    "domain": TEST_DOMAIN,
    "external_id": TEST_EXTERNAL_ID,
    "subjects": [
        {
            "start_time": (NOW - timedelta(days=3)).strftime(TIMEFORMAT),
            "end_time": (NOW + timedelta(days=30)).strftime(TIMEFORMAT),
            "registration_number": "TES71"

        }],
    "areas": [
        {
            "start_time": (NOW - timedelta(days=3)).strftime(TIMEFORMAT),
            "end_time": (NOW + timedelta(days=30)).strftime(TIMEFORMAT),
            "area": TEST_PERMIT_AREA_IDENTIFIER_1
        }]
}


def test_get_list_of_parking_permits():
    response = requests.get(f"{PARKKI_HOST}/operator/v1/permit/", headers=HEADERS)
    assert response.status_code == 200
    json_data = response.json()
    assert "count" in json_data
    assert "next" in json_data
    assert "previous" in json_data
    assert "results" in json_data


def test_create_a_permit_object(data=DATA):
    response = requests.post(f"{PARKKI_HOST}/operator/v1/permit/", headers=HEADERS, json=data)
    assert response.status_code == 201
    json_data = response.json()
    assert value_in_list_of_dicts(data["subjects"][0]["registration_number"], json_data["subjects"])
    assert value_in_list_of_dicts(TEST_PERMIT_AREA_IDENTIFIER_1, json_data["areas"])
    assert json_data["external_id"] == TEST_EXTERNAL_ID
    return json_data["id"]


def test_get_details_of_a_permit(id):
    response = requests.get(f"{PARKKI_HOST}/operator/v1/permit/{id}/", headers=HEADERS)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["id"] == id
    assert json_data["external_id"] == TEST_EXTERNAL_ID
    assert json_data["domain"] == TEST_DOMAIN
    assert value_in_list_of_dicts(DATA["subjects"][0]["registration_number"], json_data["subjects"])
    assert value_in_list_of_dicts(TEST_PERMIT_AREA_IDENTIFIER_1, json_data["areas"])


def test_replace_a_permit(id):
    data = deepcopy(DATA)
    data["id"] = 999999
    data["subjects"][0]["registration_number"] = "REP71"
    response = requests.put(f"{PARKKI_HOST}/operator/v1/permit/{id}/", headers=HEADERS, json=data)
    assert response.status_code == 200
    json_data = response.json()
    # Note, changing ID is not possible
    assert json_data["id"] == id
    assert json_data["external_id"] == TEST_EXTERNAL_ID
    assert json_data["domain"] == TEST_DOMAIN
    assert value_in_list_of_dicts(data["subjects"][0]["registration_number"], json_data["subjects"])
    assert value_in_list_of_dicts(TEST_PERMIT_AREA_IDENTIFIER_1, json_data["areas"])


def test_update_a_permit(id):
    data = deepcopy(DATA)
    data["subjects"][0]["registration_number"] = "UPP42"
    response = requests.patch(f"{PARKKI_HOST}/operator/v1/permit/{id}/", headers=HEADERS, json=data)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["id"] == id
    assert json_data["external_id"] == TEST_EXTERNAL_ID
    assert json_data["domain"] == TEST_DOMAIN
    assert value_in_list_of_dicts(data["subjects"][0]["registration_number"], json_data["subjects"])
    assert value_in_list_of_dicts(TEST_PERMIT_AREA_IDENTIFIER_1, json_data["areas"])


def test_list_of_permits_in_active_series():
    response = requests.get(f"{PARKKI_HOST}/operator/v1/activepermit/", headers=HEADERS)
    response.status_code == 200
    json_data = response.json()
    assert "count" in json_data
    assert "next" in json_data
    assert "previous" in json_data
    assert "results" in json_data


def test_create_permit_to_the_active_series(data=DATA):
    response = requests.post(f"{PARKKI_HOST}/operator/v1/activepermit/", headers=HEADERS, json=data)
    assert response.status_code == 201
    json_data = response.json()
    assert json_data
    assert value_in_list_of_dicts(data["subjects"][0]["registration_number"], json_data["subjects"])
    assert value_in_list_of_dicts(TEST_PERMIT_AREA_IDENTIFIER_1, json_data["areas"])
    assert json_data["external_id"] == TEST_EXTERNAL_ID
    return json_data["id"]


def test_update_a_permit_in_the_active_series(id, data=DATA):
    data["subjects"][0]["registration_number"] = "UPP42"
    response = requests.patch(f"{PARKKI_HOST}/operator/v1/activepermit/{id}/", headers=HEADERS, json=data)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["external_id"] == TEST_EXTERNAL_ID
    assert json_data["domain"] == TEST_DOMAIN
    assert value_in_list_of_dicts(DATA["subjects"][0]["registration_number"], json_data["subjects"])
    assert value_in_list_of_dicts(TEST_PERMIT_AREA_IDENTIFIER_1, json_data["areas"])


def test_replace_a_permit_in_the_active_series(id, data=DATA):
    data["subjects"][0]["registration_number"] = "REP71"
    response = requests.put(f"{PARKKI_HOST}/operator/v1/activepermit/{id}/", headers=HEADERS, json=data)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["external_id"] == TEST_EXTERNAL_ID
    assert json_data["domain"] == TEST_DOMAIN
    assert value_in_list_of_dicts(DATA["subjects"][0]["registration_number"], json_data["subjects"])
    assert value_in_list_of_dicts(TEST_PERMIT_AREA_IDENTIFIER_1, json_data["areas"])


def test_get_details_of_a_activepermit(id):
    response = requests.get(f"{PARKKI_HOST}/operator/v1/activepermit/{id}/", headers=HEADERS)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["external_id"] == TEST_EXTERNAL_ID
    assert json_data["domain"] == TEST_DOMAIN
    assert value_in_list_of_dicts(DATA["subjects"][0]["registration_number"], json_data["subjects"])
    assert value_in_list_of_dicts(TEST_PERMIT_AREA_IDENTIFIER_1, json_data["areas"])


def test_delete_a_permit(id):
    response = requests.delete(f"{PARKKI_HOST}/operator/v1/permit/{id}/", headers=HEADERS)
    assert response.status_code == 204


def test_delete_a_permit_in_active_series(id):
    response = requests.delete(f"{PARKKI_HOST}/operator/v1/activepermit/{id}/", headers=HEADERS)
    assert response.status_code == 204


if __name__ == "__main__":
    # In case of test failure, delete obsolete permits as it will try to create duplicates
    # test_delete_a_permit_in_active_series(TEST_EXTERNAL_ID)
    # test_delete_a_permit(183)

    # Test Permits
    test_get_list_of_parking_permits()
    id = test_create_a_permit_object()
    test_get_details_of_a_permit(id)
    test_replace_a_permit(id)
    test_update_a_permit(id)
    test_delete_a_permit(id)

    # Test ActivePermits
    test_list_of_permits_in_active_series()
    test_create_permit_to_the_active_series()
    test_get_details_of_a_activepermit(TEST_EXTERNAL_ID)
    test_update_a_permit_in_the_active_series(TEST_EXTERNAL_ID)
    test_replace_a_permit_in_the_active_series(TEST_EXTERNAL_ID)
    test_delete_a_permit_in_active_series(TEST_EXTERNAL_ID)
