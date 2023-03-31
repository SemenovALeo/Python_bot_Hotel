import datetime

import database.models
from api import api
from database import models
from telebot.types import InputMediaPhoto

def get_datetime_str(value):
    data_value = datetime.datetime.strptime(value, '%d/%m/%y')
    data = {'day':data_value.date().day,
            'month':data_value.date().month,
            'year':data_value.date().year}
    return data


def gef_foto(data):
    value = data['propertyGallery']['images']
    foto = []
    count = 0
    for i in value:
        if count < 3:
            foto.append(i['image']['url'])
            count += 1
        else:
            break

    return foto

def get_hotels(data):
    responce = api.api_request('properties/v2/list',data,'POST')
    if responce:
        hotels = list()
        for dest in responce['data']['propertySearch']['properties']:
            hotels.append({'id': dest['id'],'name': dest['name']})
    else:
        hotels = list({'id': '2', 'name': 'Ответа нет, вернитесь назад'})

    if data['command'] == '/highprice':
        hotels.reverse()

    return hotels

def text_output(bot,call):
    hotel_detail = api.api_request('properties/v2/detail', call.data, 'POST')['data']['propertyInfo']
    name_Hotel = hotel_detail['summary']['name']
    address_Line = hotel_detail['summary']['location']['address']['addressLine']
    website = f'https://www.hotels.com/h{call.data}.Hotel-Information'
    photos = gef_foto(hotel_detail)
    with bot.retrieve_data(call.from_user.id) as data:
        data['hotelName'] = name_Hotel

    hotel_list = api.api_request('properties/v2/list', data, 'POST')['data']['propertySearch']['properties'][0]
    price = hotel_list['price']['lead']['formatted']
    distance = hotel_list['destinationInfo']['distanceFromDestination']['value']
    medias = []

    for foto in photos:
        medias.append(InputMediaPhoto(foto))

    bot.send_media_group(call.from_user.id, medias)
    bot.send_message(call.from_user.id, f'<b>Название:</b> {name_Hotel}\n'
                                        f'<b>Адресс: </b> {address_Line}\n'
                                        f'<b>Расположению от центра: </b> {distance} миль\n'
                                        f'<b>Цена: </b> {price}\n'
                                        f'<b>Сайт: </b> {website}'
                     , parse_mode='Html')
    setter_bd(call, data, name_Hotel, address_Line, distance, price, website)

def setter_bd(call, data, name_Hotel, address_Line, distance, price, website ):

    User_new, created = models.User.get_or_create(
        user_id = call.from_user.id,
        username = call.from_user.username
    )

    Order = models.Order(
        user_id = User_new,
        command= data['command'],
        city=data['city'],
        quantity_hotel=data['quantity_hotel'],
        check_in=f"{data['check_in']['day']}.{data['check_in']['month']}."
                 f"{data['check_in']['year']}",
        check_out=f"{data['check_out']['day']}.{data['check_out']['month']}."
                  f"{data['check_out']['year']}",
        adults=data['adults'],
    ).save()

    Exception = models.Extradition(
        User_id = User_new,
        command_id = Order,
        name=name_Hotel,
        address=address_Line,
        distance=distance,
        price=price,
        website=website
    ).save()
