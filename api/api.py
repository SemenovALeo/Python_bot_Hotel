import requests
import json
from config_data import config
from requests import get
from requests import post

# method_endswith = 'locations/v3/search'
# method_type = 'GET'
# querystring = {'city': 'Рим', 'language': 'ru_RU', 'quantity_hotel': '2', 'check_in': '54', 'check_out': '45', 'adults': '2', 'children': '1'}
#
# url = f"https://hotels4.p.rapidapi.com{method_endswith}"

def api_request(method_endswith,  # Меняется в зависимости от запроса. locations/v3/search либо properties/v2/list
                params,  # Параметры, если locations/v3/search, то {'q': 'Рига', 'locale': 'ru_RU'}
                method_type  # Метод\тип запроса GET\POST
                ):
    print(params)
    url = f"https://hotels4.p.rapidapi.com/{method_endswith}"
    # Определяем тип параметра
    if method_endswith == 'locations/v3/search':
        params = {"q":f"{params['city']}","locale":f"{params['language']}","langid":"1033","siteid":"300000001"}
    elif method_endswith == 'properties/v2/list':
        params = {
            "currency": "USD",
            "eapid": 1,
            "locale": f"{params['language']}",
            "siteId": 300000001,
            "destination": {"regionId": f"{params['gaiaId']}"},
            "checkInDate": {
                "day": f"{params['check_in']['day']}",
                "month": f"{params['check_in']['month']}",
                "year": f"{params['check_in']['year']}"
            },
            "checkOutDate": {
                "day": f"{params['check_out']['day']}",
                "month": f"{params['check_out']['month']}",
                "year": f"{params['check_out']['year']}"
            },
            "rooms": [
                {
                    "adults": f"{params['adults']}",
                }
            ],
            "resultsStartingIndex": 0,
            "resultsSize": f"{params['quantity_hotel']}",
            "sort": "PRICE_LOW_TO_HIGH",
            "filters": {'availableFilter': 'SHOW_AVAILABLE_ONLY'}
        }


    # В зависимости от типа запроса вызываем соответствующую функцию
    if method_type == 'GET':
        return get_request(
            url=url,
            params=params
        )
    else:
        return post_request(
            url=url,
            params=params
        )


def get_request(url, params):
    try:
        response = get(
            url,
            headers={
	"X-RapidAPI-Key": f"{config.RAPID_API_KEY}",
	"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
},
            params=params,
            timeout=100
        )
        if response.status_code == requests.codes.ok:
            return json.loads(response.text)
    except ValueError:
        print('Нет соедениние с API хостом')

def post_request(url, params):
    try:
        response = post(
            url,
            json=params,
            headers={
                "content-type": "application/json",
                "X-RapidAPI-Key": f"{config.RAPID_API_KEY}",
                "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
            },
            timeout=100
        )
        if response.status_code == requests.codes.ok:
            return json.loads(response.text)
    except ValueError:
        print('Нет соедениние с API хостом')




