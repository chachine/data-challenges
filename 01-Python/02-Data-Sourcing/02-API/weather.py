# pylint: disable=missing-module-docstring

import sys
import urllib.parse
import requests

BASE_URI = "https://weather.lewagon.com"


def search_city(query):
    '''Look for a given city. If multiple options are returned, have the user choose between them.
       Return one city (or None)
    '''
    # $CHALLENGIFY_BEGIN
    url = urllib.parse.urljoin(BASE_URI, "/geo/1.0/direct")
    cities = requests.get(url, params={'q': query}).json()
    if not cities:
        print(f"Sorry, OpenWeather does not know about {query}...")
        return None
    if len(cities) == 1:
        return cities[0]
    for i, city in enumerate(cities):
        print(f"{i + 1}. {city['title']}")
    index = int(input("Oops, which one did you mean?")) - 1
    return cities[index]
    # $CHALLENGIFY_END


def weather_forecast(lat, lon):
    '''Return a 5-day weather forecast for the city, given its latitude and longitude.'''
    # $CHALLENGIFY_BEGIN
    url = urllib.parse.urljoin(BASE_URI, "/data/2.5/forecast")
    forecasts = requests.get(
        url, params={'lat': lat, 'lon': lon, 'units': 'metric'}).json()['list']
    return forecasts[::8]
    # $CHALLENGIFY_END


def main():
    '''Ask user for a city and display weather forecast'''
    query = input("City?\n> ")
    city = search_city(query)
    # TODO: Display weather forecast for a given city
    # $CHALLENGIFY_BEGIN
    if city:
        daily_forecasts = weather_forecast(city['lat'], city['lon'])
        for forecast in daily_forecasts:
            max_temp = round(forecast['main']['temp_max'])
            print(
                f"{forecast['dt_txt'][:10]}: {forecast['weather'][0]['main']} ({max_temp}°C)")
    # $CHALLENGIFY_END


if __name__ == '__main__':
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print('\nGoodbye!')
        sys.exit(0)
