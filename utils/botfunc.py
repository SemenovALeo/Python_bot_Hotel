import datetime
from loader import bot
from api import api

def get_datetime_str(value):
    data_value = datetime.datetime.strptime(value, '%d/%m/%y')
    data = {'day':data_value.date().day,
            'month':data_value.date().month,
            'year':data_value.date().year}
    return data

def get_id_region(data):
    print(data)
    # print(api.api_request('properties/v2/list',data,'POST')['data']['propertySearch']['properties'])

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



    # print(foto_hotel)



# for obj in list_hotel:
#     if user.photos.isdigit():
#         medias = [ types.InputMediaPhoto(media, caption=obj[0][0])
#             if index == 0 else types.InputMediaPhoto(media) for index, media in enumerate(flatten(obj[1]))]       bot.send_media_group(chat_id, medias)
#     else:        bot.send_message(chat_id, obj)