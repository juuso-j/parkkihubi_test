from copy import deepcopy
from datetime import datetime, timedelta

import requests
from constants import (
    HEADERS, PARKKI_HOST, TEST_DOMAIN, TEST_EXTERNAL_ID,
    TEST_PAYMENT_ZONE_NUMBER, TEST_PERMIT_AREA_IDENTIFIER_1,
    TEST_PERMIT_AREA_IDENTIFIER_2, TEST_PERMIT_SERIES_ID, TIMEFORMAT)
from utils import value_in_list_of_dicts

NOW = datetime.now()
TEST_REG_NUM = "TES7"
PARKING_DATA = {
    "zone": TEST_PAYMENT_ZONE_NUMBER,
    "domain": TEST_DOMAIN,
    "location": {
        "type": "Point",
        "coordinates": [
            22.2621559,
            60.4525144
        ]
    },
    "registration_number": TEST_REG_NUM,
}
PERMIT_DATA = {
    "series": TEST_PERMIT_SERIES_ID,
    # "domain": TEST_DOMAIN,
    "external_id": TEST_EXTERNAL_ID,
    "subjects": [
        {
            "start_time": (NOW - timedelta(days=3)).strftime(TIMEFORMAT),
            "end_time": (NOW + timedelta(days=30)).strftime(TIMEFORMAT),
            "registration_number": PARKING_DATA["registration_number"]

        }],
    "areas": [
        {
            "start_time": (NOW - timedelta(days=3)).strftime(TIMEFORMAT),
            "end_time": (NOW + timedelta(days=30)).strftime(TIMEFORMAT),
            "area": TEST_PERMIT_AREA_IDENTIFIER_1
        }]
}


def create_a_permit_object(data=PERMIT_DATA):
    response = requests.post(f"{PARKKI_HOST}/enforcement/v1/permit/", headers=HEADERS, json=data)
    assert response.status_code == 201
    return response.json()["id"]


def delete_a_permit(id):
    response = requests.delete(f"{PARKKI_HOST}/enforcement/v1/permit/{id}/", headers=HEADERS)
    assert response.status_code == 204


def create_valid_parking(data=PARKING_DATA):
    data["time_start"] = (NOW - timedelta(hours=4)).strftime(TIMEFORMAT)
    data["time_end"] = (NOW + timedelta(days=1, hours=1)).strftime(TIMEFORMAT)
    response = requests.post(f"{PARKKI_HOST}/operator/v1/parking/", headers=HEADERS, json=data)
    assert response.status_code == 201
    json_data = response.json()
    assert json_data["status"] == "valid"
    return json_data["id"]


def delete_parking(id):
    response = requests.delete(f"{PARKKI_HOST}/operator/v1/parking/{id}/", headers=HEADERS)
    assert response.status_code == 204


def delete_permit_series_object(id):
    response = requests.delete(f"{PARKKI_HOST}/operator/v1/permitseries/{id}/", headers=HEADERS)
    assert response.status_code == 204


def test_get_valid_parking_unauthorization():
    headers = deepcopy(HEADERS)
    headers["Authorization"] = "ApiKey foo42"
    response = requests.get(f"{PARKKI_HOST}/enforcement/v1/valid_parking/", headers=headers)
    assert response.status_code == 401


def test_get_valid_parkings_no_parameters():
    response = requests.get(f"{PARKKI_HOST}/enforcement/v1/valid_parking/", headers=HEADERS)
    assert response.status_code == 400
    assert "Either time or registration number required" in response.text


def test_get_valid_parkings():
    time = (datetime.now() - timedelta(days=1)).strftime(TIMEFORMAT)
    response = requests.get(f"{PARKKI_HOST}/enforcement/v1/valid_parking/?time={time}", headers=HEADERS)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["count"] > 0
    assert "next" in json_data
    assert "previous" in json_data
    assert "results" in json_data


def test_get_valid_parking_non_existing():
    response = requests.get(f"{PARKKI_HOST}/enforcement/v1/valid_parking/?reg_num=TES713", headers=HEADERS)
    assert response.status_code == 200
    assert response.json()["count"] == 0


def test_get_valid_parking_existing():
    response = requests.get(
        f"{PARKKI_HOST}/enforcement/v1/valid_parking/?reg_num={PARKING_DATA['registration_number']}", headers=HEADERS)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["count"] > 0
    assert "created_at" in json_data["results"][0]
    assert "modified_at" in json_data["results"][0]
    assert "registration_number" in json_data["results"][0]
    assert "time_start" in json_data["results"][0]
    assert "time_end" in json_data["results"][0]
    assert "zone" in json_data["results"][0]
    assert "operator" in json_data["results"][0]
    assert "operator_name" in json_data["results"][0]


def test_get_list_of_valid_permit_items():
    response = requests.get(f"{PARKKI_HOST}/enforcement/v1/valid_permit_item/?reg_num={TEST_REG_NUM}", headers=HEADERS)
    assert response.status_code == 200
    json_data = response.json()
    assert len(json_data["results"]) > 0
    assert value_in_list_of_dicts(PARKING_DATA["registration_number"], json_data["results"]) is True
    assert "id" in json_data["results"][0]
    assert "permit_id" in json_data["results"][0]
    assert "area" in json_data["results"][0]
    assert "registration_number" in json_data["results"][0]
    assert "start_time" in json_data["results"][0]
    assert "end_time" in json_data["results"][0]
    assert "operator" in json_data["results"][0]
    assert "operator_name" in json_data["results"][0]
    assert "properties" in json_data["results"][0]


def test_list_of_parking_operators():
    response = requests.get(f"{PARKKI_HOST}/enforcement/v1/operator/", headers=HEADERS)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["count"] > 0
    assert "next" in json_data
    assert "previous" in json_data
    assert len(json_data["results"]) > 0
    return json_data["results"][0]["id"]


def test_get_details_of_a_parking_operator(id):
    response = requests.get(f"{PARKKI_HOST}/enforcement/v1/operator/{id}/", headers=HEADERS)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["id"] == id
    assert "created_at" in json_data
    assert "modified_at" in json_data
    assert "name" in json_data


def test_get_list_of_permit_series():
    response = requests.get(f"{PARKKI_HOST}/enforcement/v1/permitseries/", headers=HEADERS)
    assert response.status_code == 200
    json_data = response.json()
    assert "count" in json_data
    assert "next" in json_data
    assert "previous" in json_data
    assert "results" in json_data
    assert json_data["count"] > 0
    assert len(json_data["results"]) > 0


def test_create_a_permit_series_object():
    data = {}
    response = requests.post(f"{PARKKI_HOST}/enforcement/v1/permitseries/", headers=HEADERS, json=data)
    assert response.status_code == 201
    json_data = response.json()
    assert "created_at" in json_data
    assert "modified_at" in json_data
    assert json_data["active"] is False
    return json_data["id"]


def test_get_details_of_permit_series(id):
    response = requests.get(f"{PARKKI_HOST}/enforcement/v1/permitseries/{id}/", headers=HEADERS)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["id"] == id
    assert "created_at" in json_data
    assert "modified_at" in json_data
    assert json_data["active"] is False


def test_activate_a_permit_series(id):
    data = {}
    response = requests.post(f"{PARKKI_HOST}/enforcement/v1/permitseries/{id}/activate/", headers=HEADERS, data=data)
    assert response.status_code == 200
    assert response.json()["status"] == "OK"
    response = requests.get(f"{PARKKI_HOST}/enforcement/v1/permitseries/{id}/", headers=HEADERS)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["id"] == id
    assert json_data["active"] is True
    response = requests.post(f"{PARKKI_HOST}/enforcement/v1/permitseries/{id}/activate/", headers=HEADERS, data=data)
    assert response.status_code == 200
    assert response.json()["status"] == "No change"


def test_get_list_of_your_parking_permits():
    response = requests.get(f"{PARKKI_HOST}/enforcement/v1/permit/", headers=HEADERS)
    assert response.status_code == 200
    json_data = response.json()
    assert "count" in json_data
    assert "next" in json_data
    assert "previous" in json_data
    assert "results" in json_data
    assert json_data["count"] > 0
    assert len(json_data["results"]) > 0


def test_create_a_permit_object():
    data = deepcopy(PERMIT_DATA)
    data["areas"][0]["area"] = "unknown"
    response = requests.post(f"{PARKKI_HOST}/enforcement/v1/permit/", headers=HEADERS, json=data)
    assert response.status_code == 400
    assert "Unknown identifiers" in response.text

    data["areas"][0]["area"] = TEST_PERMIT_AREA_IDENTIFIER_1
    response = requests.post(f"{PARKKI_HOST}/enforcement/v1/permit/", headers=HEADERS, json=data)
    assert response.status_code == 201
    json_data = response.json()
    assert value_in_list_of_dicts(data["subjects"][0]["registration_number"], json_data["subjects"])
    assert value_in_list_of_dicts(TEST_PERMIT_AREA_IDENTIFIER_1, json_data["areas"])
    assert json_data["external_id"] == TEST_EXTERNAL_ID
    return json_data["id"]


def test_get_details_of_a_permit(id):
    response = requests.get(f"{PARKKI_HOST}/enforcement/v1/permit/{id}/", headers=HEADERS)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["id"] == id
    assert json_data["subjects"][0]["registration_number"] == TEST_REG_NUM


def test_replace_a_permit(id, data=PERMIT_DATA):
    response = requests.put(f"{PARKKI_HOST}/enforcement/v1/permit/{id}/", headers=HEADERS, json=data)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["id"] == id
    assert json_data["subjects"][0]["registration_number"] == TEST_REG_NUM


def test_update_a_permit(id, data=PERMIT_DATA):
    response = requests.patch(f"{PARKKI_HOST}/enforcement/v1/permit/{id}/", headers=HEADERS, json=data)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["id"] == id
    assert json_data["subjects"][0]["registration_number"] == TEST_REG_NUM


def test_create_a_permit_to_the_active_series(data=PERMIT_DATA):
    response = requests.post(f"{PARKKI_HOST}/enforcement/v1/active_permit_by_external_id/", headers=HEADERS, json=data)
    assert response.status_code == 201
    json_data = response.json()
    assert "series" in json_data
    assert json_data["external_id"] == TEST_EXTERNAL_ID
    assert value_in_list_of_dicts(data["subjects"][0]["registration_number"], json_data["subjects"])
    return json_data["id"]


def test_get_list_of_permits_in_the_active_series():
    response = requests.get(f"{PARKKI_HOST}/enforcement/v1/active_permit_by_external_id/", headers=HEADERS)
    assert response.status_code == 200
    json_data = response.json()
    assert "count" in json_data
    assert "next" in json_data
    assert "previous" in json_data
    assert "results" in json_data
    assert json_data["count"] > 0
    assert len(json_data["results"]) > 0


def test_get_details_of_a_permit_in_the_active_series(id):
    response = requests.get(f"{PARKKI_HOST}/enforcement/v1/active_permit_by_external_id/{id}/", headers=HEADERS)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["external_id"] == id
    assert value_in_list_of_dicts(PERMIT_DATA["subjects"][0]["registration_number"], json_data["subjects"])


def test_update_a_permit_in_the_active_series(id):
    data = deepcopy(PERMIT_DATA)
    data["areas"][0]["area"] = TEST_PERMIT_AREA_IDENTIFIER_2
    response = requests.patch(
        f"{PARKKI_HOST}/enforcement/v1/active_permit_by_external_id/{id}/", headers=HEADERS, json=data)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["areas"][0]["area"] == TEST_PERMIT_AREA_IDENTIFIER_2
    assert json_data["external_id"] == id
    assert value_in_list_of_dicts(PERMIT_DATA["subjects"][0]["registration_number"], json_data["subjects"])


def test_replace_a_permit_in_the_active_series(id):
    data = deepcopy(PERMIT_DATA)
    data["areas"][0]["area"] = TEST_PERMIT_AREA_IDENTIFIER_2
    response = requests.patch(
        f"{PARKKI_HOST}/enforcement/v1/active_permit_by_external_id/{id}/", headers=HEADERS, json=data)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["areas"][0]["area"] == TEST_PERMIT_AREA_IDENTIFIER_2
    assert json_data["external_id"] == id
    assert value_in_list_of_dicts(PERMIT_DATA["subjects"][0]["registration_number"], json_data["subjects"])


if __name__ == "__main__":
    # In case of test failure, delete the created permit and parking
    delete_a_permit(181)
    # delete_parking(parking_id)
    parking_id = create_valid_parking()
    test_get_valid_parking_unauthorization()
    test_get_valid_parkings_no_parameters()
    test_get_valid_parkings()
    test_get_valid_parking_non_existing()
    test_get_valid_parking_existing()
    permit_id = create_a_permit_object()
    test_get_list_of_valid_permit_items()
    first_operator_id = test_list_of_parking_operators()
    test_get_details_of_a_parking_operator(first_operator_id)
    test_get_list_of_permit_series()
    permit_series_id = test_create_a_permit_series_object()
    test_get_details_of_permit_series(permit_series_id)
    test_activate_a_permit_series(permit_series_id)
    test_get_list_of_your_parking_permits()
    delete_a_permit(permit_id)

    test_permit_object_id = test_create_a_permit_object()
    test_get_details_of_a_permit(test_permit_object_id)
    test_replace_a_permit(test_permit_object_id)
    test_update_a_permit(test_permit_object_id)
    active_permit_id = test_create_a_permit_to_the_active_series()
    test_get_list_of_permits_in_the_active_series()
    test_get_details_of_a_permit_in_the_active_series(TEST_EXTERNAL_ID)
    test_update_a_permit_in_the_active_series(TEST_EXTERNAL_ID)
    test_replace_a_permit_in_the_active_series(TEST_EXTERNAL_ID)

    delete_a_permit(test_permit_object_id)
    delete_a_permit(active_permit_id)
    delete_parking(parking_id)
    delete_permit_series_object(permit_series_id)
