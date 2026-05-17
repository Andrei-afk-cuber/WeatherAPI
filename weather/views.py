from django.core.cache import cache
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import UserRequest
from .utils import get_weather
from .serializers import WeatherSerializer, WeatherRequestsHistorySerializer


# view for weather
class WeatherView(APIView):
    throttle_classes = [AnonRateThrottle]

    def get(self,request):
        city = request.GET.get('city')
        temp_measure_unit = request.GET.get('unit')

        if not city:
            return Response({'error':'add correct city at query params'}, status=status.HTTP_400_BAD_REQUEST)

        # cache
        cache_key = f'weather_{city}_{temp_measure_unit}'
        cached_data = cache.get(cache_key)

        if cached_data:
            cached_data['from_cache'] = True

            return Response(cached_data, status=status.HTTP_200_OK)

        # get new data
        weather_data = get_weather(city, temp_measure_unit)
        weather_data['city'] = city
        serializer = WeatherSerializer(data=weather_data)

        if serializer.is_valid():
            # create cache
            cache.set(cache_key, serializer.validated_data, 60*5)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# get requests history view
class RequestsHistoryView(ListAPIView):
    queryset = UserRequest.objects.all()
    serializer_class = WeatherRequestsHistorySerializer

    # override for filters
    def get_queryset(self):
        queryset = self.queryset
        # filters
        city = self.request.GET.get('city')
        from_date = self.request.GET.get('from')
        to_date = self.request.GET.get('to')

        if city:
            queryset = queryset.filter(city__icontains=city)

        if from_date:
            queryset = queryset.filter(created_at__gte=from_date)

        if to_date:
            queryset = queryset.filter(created_at__lte=to_date)

        return queryset