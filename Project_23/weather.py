import requests
from pprint import pprint
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the API key from the .env file
API_Key = os.getenv('API_KEY')

# Prompt the user for a city name
city = input('Enter city name: ')

# Build the API request URL
base_url = f'http://api.openweathermap.org/data/2.5/weather?appid={API_Key}&q={city}'

# Make the API request
response = requests.get(base_url)

# Handle the response
if response.status_code == 200:
    weather_data = response.json()
    pprint(weather_data)
else:
    print(f"Error: Unable to fetch weather data. HTTP Status Code: {response.status_code}")