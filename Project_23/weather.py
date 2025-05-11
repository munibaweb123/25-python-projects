import requests

from pprint import pprint

API_Key = '1397ef5f01d4fea55b5957ba49e9b807'


city = input('Enter city name: ')

base_url = f'http://api.openweathermap.org/data/2.5/weather?appid={API_Key}&q={city}'

weather_data = requests.get(base_url).json()

pprint(weather_data)