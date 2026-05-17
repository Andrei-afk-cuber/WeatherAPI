from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .utils import get_weather
from .serializers import WeatherSerializer

# view for weather
class WeatherView(APIView):
    def get(self,request):
        city = request.GET.get('city')

        if city:
            try:
                weather_data = get_weather(city)
                weather_data['city'] = city

                serializer = WeatherSerializer(data=weather_data)

                if serializer.is_valid():
                    return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': 'e'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'error':'add correct city at query params'}, status=status.HTTP_400_BAD_REQUEST)