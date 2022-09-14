import requests
from config.config import settings

def get_readings(url, body):

    response = requests.get(url, json = body)
    data = response.json()

    return data 