import pytest, sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.controllers.openweather import get_coord_from_city

def test_get_coord_from_city_fail():
    location1 = ""
    res = get_coord_from_city(location1)
    assert res.status_code == 400

def test_get_coord_from_city_fail_with_invalid_city():
    location1 = "InvalidCityName12345"
    res = get_coord_from_city(location1)
    assert res.status_code == 404


def test_get_coord_from_city_success():
    location2 = "Paris"
    assert get_coord_from_city(location2).name is not None
    assert get_coord_from_city(location2).country is not None
    assert get_coord_from_city(location2).lon is not None
    assert get_coord_from_city(location2).lat is not None
