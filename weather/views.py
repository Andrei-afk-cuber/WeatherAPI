import csv
from django.core.cache import cache
from django.http import HttpResponse
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView
from rest_framework.response import Response
import logging

from .models import UserRequest
from .utils import get_weather
from .serializers import WeatherSerializer, WeatherRequestsHistorySerializer

# create logger
logger = logging.getLogger(__name__)

# view for weather
class WeatherView(APIView):
    throttle_classes = [AnonRateThrottle]

    def get(self,request):
        city = request.GET.get('city')
        temp_measure_unit = request.GET.get('unit')

        logger.info(f'Request started, city = {city}')

        if not city:
            logger.warning(f'Request failed: missing city parameter')
            return Response({'error':'add correct city at query params'}, status=status.HTTP_400_BAD_REQUEST)

        # cache
        cache_key = f'weather_{city}_{temp_measure_unit}'
        cached_data = cache.get(cache_key)

        if cached_data:
            logger.info(f'City is taken from cache ({cache_key})')
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

            logger.info(f'Request successful for city {city}')
            return Response(serializer.data, status=status.HTTP_200_OK)

        logger.error(f'Request failed for city {city}. Error: {serializer.errors}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# get requests history view
class RequestsHistoryView(ListAPIView):
    queryset = UserRequest.objects.all()
    serializer_class = WeatherRequestsHistorySerializer

    # override for filters
    def get_queryset(self):
        queryset = super().get_queryset().order_by('id')

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

    def get(self, request, *args, **kwargs):
        logger.info(f'History request, params: {request.GET}')
        format_type = request.GET.get('export')

        if format_type == 'csv':
            logger.info(f'Exporting to CSV.')
            return self._csv_export()

        return super().list(request, *args, **kwargs)

    # method for create csv export
    def _csv_export(self):
        queryset = self.get_queryset()

        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="weather-history.csv"'

        writer = csv.writer(response)

        writer.writerow([
            'Id',
            'city',
            'weather',
            'weather description',
            'temperature',
            'temp_measure_unit',
            'created at',
        ])

        for obj in queryset:
            writer.writerow([
                obj.id,
                obj.city,
                obj.weather,
                obj.weather_description,
                obj.temperature,
                obj.temp_measure_unit,
                obj.created_at,
            ])

        logger.info(f'CSV export complete')
        return response