import requests
import time
import logging

from config import APIConfig


logger = logging.getLogger(__name__)


# function for get weather
def get_weather(city, temp_measure="C"):
    result = {}
    start = time.time()
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "appid": APIConfig.API_KEY,
        "q": city,
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        duration = (time.time() - start) * 1000

        logger.info(
            f"External API call duration: {duration:.2f}ms. Status: {response.status_code}"
        )

        # data processing
        if response.status_code == 200:
            weather_data = response.json()
            result["temp_measure_unit"] = temp_measure.upper()

            if result["temp_measure_unit"] == "C":
                result["temperature"] = round(weather_data["main"]["temp"] - 273.15)
            else:
                result["temp_measure_unit"] = "F"
                result["temperature"] = round(weather_data["main"]["temp"])

            result = result | weather_data["weather"][0]

            return result

        logger.error(f"External API for city error: {response.status_code}")
        return {"error": response.status_code}
    except requests.exceptions.Timeout:
        logger.error("External API timeout")
        return {"error": "timeout"}
    except requests.exceptions.ConnectionError:
        logger.error("External API connection error")
        return {"error": "connection error"}
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return {"error": str(e)}
