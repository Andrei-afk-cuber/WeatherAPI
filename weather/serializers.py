from rest_framework import serializers

from .models import UserRequest

class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRequest
        fields = ['city', 'weather', 'weather_description', 'temperature']

    def to_internal_value(self, data):
        return {
            'city': data.get('city'),
            'weather': data.get('main'),
            'temperature': data.get('temperature'),
            'weather_description': data.get('description'),
        }

class WeatherRequestsHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRequest
        fields = '__all__'