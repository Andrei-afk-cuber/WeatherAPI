import datetime

from django.core.cache import cache
import pytest
from pytest_factoryboy import register

from tests.factories import RequestFactory


# fixture for get cities list
@pytest.fixture(scope='session')
def cities():
    return [
        'Minsk',
        'Moscow',
        'Berlin',
        'Monaco',
        'Molodechno',
        'Los Angeles',
        'New York',
        'Paris',
        'Toronto',
        'San Antonio',
    ]

# fixture for clear throttle cache
@pytest.fixture(autouse=True)
def clear_throttling():
    cache.clear()

# fixture for get current date
@pytest.fixture(scope='function')
def current_date():
    return datetime.datetime.date(datetime.datetime.now())

# register here factory fixtures
register(RequestFactory)
