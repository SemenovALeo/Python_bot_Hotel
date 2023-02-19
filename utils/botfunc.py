import json

import requests
from config_data import config


def get_id_region(data):
    url = "https://hotels4.p.rapidapi.com/locations/v3/search"

    querystring = {"q": f"{data}", "locale": f"ru_RU", "langid": "1033", "siteid": "300000001"}

    headers = {
        "X-RapidAPI-Key": config.RAPID_API_KEY,
        "X-RapidAPI-Host": config.RAPID_API_HOST
    }

    response = requests.request("GET", url, headers=headers, params=querystring, timeout=10)



    dataAPI = json.loads(response.text)

    id_city = dataAPI['sr'][0]['gaiaId']

    return id_city
def get_hotel(data):
    pass