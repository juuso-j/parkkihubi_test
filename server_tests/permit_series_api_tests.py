import requests
from constants import HEADERS, PARKKI_HOST


def test_get_permit_series_list():
    response = requests.get(f"{PARKKI_HOST}/operator/v1/permitseries/", headers=HEADERS)
    assert response.status_code == 200
    json_data = response.json()
    assert "count" in json_data
    assert "results" in json_data


def test_post_not_active_permit_series():
    response = requests.post(f"{PARKKI_HOST}/operator/v1/permitseries/", headers=HEADERS, json={})
    assert response.status_code == 201
    assert response.json()["active"] is False
    return response.json()["id"]


def test_get_detail_of_permit_series(id):
    response = requests.get(f"{PARKKI_HOST}/operator/v1/permitseries/{id}/", headers=HEADERS)
    assert response.status_code == 200
    json_data = response.json()
    assert "id" in json_data
    assert "created_at" in json_data
    assert "modified_at" in json_data
    assert "active" in json_data


def test_activate_a_permit_series(id):
    response = requests.post(f"{PARKKI_HOST}/operator/v1/permitseries/{id}/activate/", headers=HEADERS)
    assert response.status_code == 200
    assert response.json()["status"] == "OK"
    response = requests.get(f"{PARKKI_HOST}/operator/v1/permitseries/{id}/", headers=HEADERS)
    assert response.status_code == 200
    assert response.json()["active"] is True


def test_delete_permit_series_by_id(id):
    response = requests.delete(f"{PARKKI_HOST}/operator/v1/permitseries/{id}/", headers=HEADERS)
    assert response.status_code == 204


if __name__ == "__main__":
    test_get_permit_series_list()
    id = test_post_not_active_permit_series()
    test_get_detail_of_permit_series(id)
    test_activate_a_permit_series(id)
    test_delete_permit_series_by_id(id)
