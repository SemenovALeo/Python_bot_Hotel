from loader import bot
from telebot.types import InputMediaPhoto
import utils.botfunc as botfunc
from api import api


@bot.callback_query_handler(func=lambda call: call.data == 'lowprice')
def low_price(call): # <- passes a CallbackQuery type object to your function
    if call.message:
        hotel_detail = api.api_request('properties/v2/detail',call.data,'POST')['data']['propertyInfo']
        name_Hotel = hotel_detail['summary']['name']
        address_Line = hotel_detail['summary']['location']['address']['addressLine']
        photos = botfunc.gef_foto(hotel_detail)
        with bot.retrieve_data(call.from_user.id) as data:
            data['hotelName'] = name_Hotel


        hotel_list = api.api_request('properties/v2/list',data,'POST')['data']['propertySearch']['properties'][0]
        price = hotel_list['price']['lead']['formatted']
        distance = hotel_list['destinationInfo']['distanceFromDestination']['value']
        medias = []

        for foto in photos:
            medias.append(InputMediaPhoto(foto))

        bot.send_media_group(call.from_user.id,medias)
        bot.send_message(call.from_user.id,f'<b>Название:</b> {name_Hotel}\n'
                                           f'<b>Адресс: </b> {address_Line}\n'
                                           f'<b>Расположению от центра: </b> {distance} миль\n'
                                           f'<b>Цена: </b> {price}\n'
                                           f'<b>Сайт: </b> https://www.hotels.com/h{call.data}.Hotel-Information'
                         ,parse_mode='Html')


