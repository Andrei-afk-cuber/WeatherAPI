import requests

KEY='354b92296ab4c0c2ed2fdd7c25343279'

# function for get weather
def get_weather(city):
    result = {}
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'appid': KEY,
        'q': city,
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        weather_data = response.json()
        result['temperature'] = round(weather_data['main']['temp'] - 273.15)
        result = result | weather_data['weather'][0]
        return result

    return {'error': response.status_code}

if __name__ == '__main__':
    print(get_weather('Minsk'))