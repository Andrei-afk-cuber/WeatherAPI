from rest_framework import serializers


class WeatherSerializer(serializers.Serializer):
    city = serializers.CharField()
    main = serializers.CharField()
    description = serializers.CharField()
    temperature = serializers.IntegerField()