import datetime
from loader import bot
from api import api

def get_datetime_str(value):
    data_value = datetime.datetime.strptime(value, '%d/%m/%y')
    data = {'day':data_value.date().day,
            'month':data_value.date().month,
            'year':data_value.date().year}
    return data


def gef_foto(data):
    value = api.api_request('properties/v2/detail',data,'POST')['data']['propertyInfo']['propertyGallery']['images']
    foto = []
    count = 0
    for i in value:
        if count < 3:
            foto.append(i['image']['url'])
            count += 1
        else:
            break

    return foto


def OutputMessage():
    pass


# def get_hotels(data):
#     responce = api.api_request('properties/v2/list',data,'POST')
#     if responce:
#         hotels = list()
#         for dest in responce['data']['propertySearch']['properties']:
#             hotels.append({'id': dest['id'],'name': dest['name']})
#     else:
#         hotels = list({'id': '2', 'name': 'Ответа нет, вернитесь назад'})
#     return hotels