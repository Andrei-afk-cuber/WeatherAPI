import pytest
import time
from django.core.cache import cache


class TestWeatherSafety:
    # test for comparison requests speed
    @pytest.mark.django_db
    def test_cache(self, client, cities):
        # check time for no cache
        start_no_cache = time.time()
        for city in cities[:5]:
            response = client.get('/weather/?city=' + city)
            assert response.status_code == 200
        end_no_cache = time.time()

        res1 = end_no_cache - start_no_cache

        # check time with cache
        start_cache = time.time()
        for _ in range(5):
            response = client.get('/weather/?city=' + 'Krasnodar')
            assert response.status_code == 200
        end_cache = time.time()

        res2 = end_cache - start_cache

        # check result
        assert res1 > res2

    # throttling test
    @pytest.mark.django_db
    def test_throttling(self, client, cities):
        # create ten first requests
        for city in cities:
            response = client.get('/weather/?city=' + city)
            assert response.status_code == 200

        response = client.get('/weather/?city=Krasnodar')

        # check status code 429
        assert response.status_code == 429
        cache.clear()

        # check records count
        response = client.get('/weather/history/')
        assert response.status_code == 200
        assert response.data['count'] == 10