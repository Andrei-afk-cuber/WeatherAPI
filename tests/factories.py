import factory
from factory.fuzzy import FuzzyChoice

from weather.models import UserRequest


# Create records factory
class RequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserRequest

    city = factory.Sequence(lambda n: f"city_{n}")
    weather = "Cloudly"
    weather_description = "Cloudly"
    temp_measure_unit = FuzzyChoice(choices=["C", "F"])
    temperature = factory.LazyAttribute(
        lambda obj: 19 if obj.temp_measure_unit == "C" else 292
    )
