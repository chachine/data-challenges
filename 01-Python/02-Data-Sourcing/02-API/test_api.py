import requests

url = "https://weather.lewagon.com/geo/1.0/direct?q=Barcelona"
response = requests.get(url).json()
city = response[0]

print(f"{city['name']}: ({city['lat']}, {city['lon']})")
lat = city['lat']
lon = city['lon']
# url_forecast = f'https://weather.lewagon.com/data/2.5/forecast/daily?lat={lat}&lon={lon}&cnt=5'
url_forecast = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid=54633ebdb5fee724d4fab9f87561640b'
response_forecast = requests.get(url_forecast).json()

for i in range(0,5):
    print(response_forecast["list"][i]["dt_txt"])
    print(response_forecast["list"][i]["weather"][0]["description"])
    print(response_forecast["list"][i]["main"]["temp"])
