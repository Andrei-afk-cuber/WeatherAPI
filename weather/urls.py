from django.urls import path

from weather.views import WeatherView, RequestsHistoryView

urlpatterns = [
    path('', WeatherView.as_view()),
    path('history/', RequestsHistoryView.as_view()),
]