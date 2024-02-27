import requests
from constants import PARKKIOPAS_HOST


def test_get_list_of_parking_areas():
    response = requests.get(f"{PARKKIOPAS_HOST}/public/v1/parking_area/")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["type"] == "FeatureCollection"
    assert "count" in json_data
    assert "next" in json_data
    assert "previous" in json_data
    assert "features" in json_data
    if json_data["count"] > 0:
        feature = json_data["features"][0]
        assert feature["type"] == "Feature"
        assert feature["geometry"]["type"] == "MultiPolygon"
        assert "capacity_estimate" in feature["properties"]
        assert len(feature["geometry"]["coordinates"]) > 0
        return feature["id"]
    return None


def test_get_list_of_parking_areas_statistics():
    response = requests.get(f"{PARKKIOPAS_HOST}/public/v1/parking_area_statistics/")
    assert response.status_code == 200
    json_data = response.json()
    assert "count" in json_data
    assert "next" in json_data
    assert "previous" in json_data
    assert "results" in json_data


def test_get_parking_area_statistics_by_id(id):
    response = requests.get(f"{PARKKIOPAS_HOST}/public/v1/parking_area_statistics/{id}/")
    assert response.status_code == 200
    json_data = response.json()
    assert "id" in json_data
    assert "current_parking_count" in json_data


if __name__ == "__main__":
    test_get_list_of_parking_areas_statistics()
    parking_area_id = test_get_list_of_parking_areas()
    if parking_area_id:
        test_get_parking_area_statistics_by_id(parking_area_id)
