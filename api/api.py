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
    url = f"https://hotels4.p.rapidapi.com/{method_endswith}"

    # Определяем тип параметра
    if method_endswith == 'locations/v3/search':
        # print(params)
        params = {"q":f"{params['city']}","locale":f"{params['language']}","langid":"1033","siteid":"300000001"}
        # print(params) обнови апи не забудь
    elif method_endswith == 'properties/v2/list':
        params = {
            "currency": "USD",
            "eapid": 1,
            "locale": str(params['language']),
            "siteId": 300000001,
            "destination": {"regionId": params['gaiaId']},
            "checkInDate": {
                "day": params['check_in']['day'],
                "month": params['check_in']['month'],
                "year": params['check_in']['year']
            },
            "checkOutDate": {
                "day": params['check_out']['day'],
                "month": params['check_out']['month'],
                "year": params['check_out']['year']
            },
            "rooms": [
                {
                    "adults": int(params['adults']),
                }
            ],
            "resultsStartingIndex": 0,
            "resultsSize": int(params['quantity_hotel']),
            "sort": "PRICE_LOW_TO_HIGH" if params['command'] != '/bestdeal' else 'PRICE_LOW_TO_HIGH|DISTANCE',
            "filters": {
                'hotelName': params['hotelName'] if 'hotelName' in params else 0,
                'availableFilter': 'SHOW_AVAILABLE_ONLY',
            }
        }
        print(params)
    elif method_endswith =='properties/v2/detail':
        params = {
            "currency": "USD",
            "eapid": 1,
            "locale": "ru_RU",
            "siteId": 300000001,
            "propertyId": params
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
            timeout=10
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
            timeout=10
        )
        if response.status_code == requests.codes.ok:
            return json.loads(response.text)
    except ValueError:
        print('Нет соедениние с API хостом')

