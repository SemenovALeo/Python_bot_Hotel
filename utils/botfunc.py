import datetime
from api import api
from database import models

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

def setter_bd(call, data, name_Hotel, address_Line, distance, price, website ):
    User_new = models.User(
        user_id=call.from_user.id,
        username=call.from_user.username,
        command=data['command'],
        city=data['city'],
        quantity_hotel=data['quantity_hotel'],
        check_in=f"{data['check_in']['day']}.{data['check_in']['month']}."
                 f"{data['check_in']['year']}",
        check_out=f"{data['check_out']['day']}.{data['check_out']['month']}."
                  f"{data['check_out']['year']}",
        adults=data['adults'],
    ).save()

    models.Order(
        user=User_new,
        name=name_Hotel,
        address=address_Line,
        distance=distance,
        price=price,
        website=website
    ).save()