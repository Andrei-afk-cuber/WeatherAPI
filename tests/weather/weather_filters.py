import pytest
import datetime

from tests.factories import RequestFactory


# check different filters
class TestWeatherFilters:
    # check city filter for history
    @pytest.mark.django_db
    def test_cities_filter(self, client):
        RequestFactory.create_batch(10)

        # check count of requests
        response = client.get("/weather/history/")
        assert response.status_code == 200
        assert response.data["count"] == 10

        # check count of requests with city_1
        city = "city_1"
        response = client.get("/weather/history/?city=" + city)

        assert response.status_code == 200
        assert response.data["count"] == 1

    @pytest.mark.django_db
    def test_cities_filter(self, client, current_date):
        RequestFactory.create_batch(10)

        # check date before
        date_before = str(current_date - datetime.timedelta(days=1))
        response = client.get("/weather/history/?to=" + date_before)

        assert response.status_code == 200
        assert response.data["count"] == 0

        # check date after
        date_after = str(current_date + datetime.timedelta(days=1))
        response = client.get("/weather/history/?from=" + date_after)

        assert response.status_code == 200
        assert response.data["count"] == 0

        # check current date
        response = client.get(f"/weather/history/?from={date_before}&to={date_after}")

        assert response.status_code == 200
        assert response.data["count"] == 10


class TestHistoryPagination:
    @pytest.mark.django_db
    def test_paginate(self, client):
        RequestFactory.create_batch(20)

        response = client.get("/weather/history/")

        assert response.status_code == 200
        assert response.data["count"] == 20
        assert len(response.data["results"]) == 10
