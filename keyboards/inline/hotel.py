from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from  api import  api


def hotel_founding(data):
    responce = api.api_request('properties/v2/list',data,'POST')['data']['propertySearch']['properties']

    if responce:
        hotels = list()
        for dest in responce:
            hotels.append({'id':dest['id'],'name': dest['name']})

    return hotels

def hotel_markup(data):
    hotels = hotel_founding(data)
    # Функция "city_founding" уже возвращает список словарей с нужным именем и id
    destinations = InlineKeyboardMarkup()
    for city in hotels:
        destinations.add(InlineKeyboardButton(text=city['name'], callback_data=str(city['id'])))
    return destinations
