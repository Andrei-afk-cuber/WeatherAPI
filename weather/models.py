from django.db import models


class UserRequest(models.Model):
    TEMPERATURE_CHOICES = (
        ("F", "Fahrenheit"),
        ("C", "Celsius"),
    )

    city = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    weather = models.CharField(max_length=100)
    weather_description = models.CharField(max_length=100)
    temperature = models.IntegerField()
    temp_measure_unit = models.CharField(
        max_length=1, choices=TEMPERATURE_CHOICES, default="C"
    )

    def __str__(self):
        return f"{self.city}: {self.weather}, {self.created_at}"

    class Meta:
        verbose_name = "Request"
        verbose_name_plural = "Requests"
