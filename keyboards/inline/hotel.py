from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from  api import  api



def hotel_founding(data):
    responce = api.api_request('properties/v2/list',data,'POST')
    # print(responce['data']['propertySearch']['properties'])
    # print(responce)

    if responce:
        hotels = list()
        for dest in responce['data']['propertySearch']['properties']:
            hotels.append({'id': dest['id'],'name': dest['name']})
    else:
        hotels = list({'id': '2', 'name': 'Ответа нет, вернитесь назад'})
    return hotels

def hotel_markup(data):
    hotels = hotel_founding(data)
    # Функция "city_founding" уже возвращает список словарей с нужным именем и id
    destinations = InlineKeyboardMarkup()
    for value in hotels:
        destinations.add(InlineKeyboardButton(text=value['name'], callback_data=f"{value['id']}"))
    return destinations
