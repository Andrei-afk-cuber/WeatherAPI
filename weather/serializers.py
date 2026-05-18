from rest_framework import serializers

from .models import UserRequest


class WeatherSerializer(serializers.ModelSerializer):
    from_cache = serializers.BooleanField(read_only=True, default=False)

    class Meta:
        model = UserRequest
        fields = [
            "city",
            "weather",
            "weather_description",
            "temperature",
            "temp_measure_unit",
            "from_cache",
        ]

    def to_internal_value(self, data):
        return {
            "city": data.get("city"),
            "weather": data.get("main"),
            "temperature": data.get("temperature"),
            "weather_description": data.get("description"),
            "temp_measure_unit": data.get("temp_measure_unit"),
        }


class WeatherRequestsHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRequest
        fields = "__all__"
