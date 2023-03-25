from keyboards.inline.hotel import hotel_markup
from loader import bot
from states.UserState import User_State
from telebot.types import Message, InputMediaPhoto
import utils.botfunc as botfunc
from api import api


@bot.callback_query_handler(func=lambda call: True)
def low_price(call): # <- passes a CallbackQuery type object to your function
    print(call)
    if call.message:
        # print(call.data)
        nameHotel = api.api_request('properties/v2/detail',call.data,'POST')['data']['propertyInfo']['summary']['name']
        addressLine = api.api_request('properties/v2/detail',call.data,'POST')['data']['propertyInfo']['summary']['location']['address']['addressLine']
        print('Я тут low')
        with bot.retrieve_data(call.from_user.id) as data:
            data['hotelName'] = nameHotel
        price = api.api_request('properties/v2/list',data,'POST')['data']['propertySearch']['properties'][0]['price']['lead']['formatted']
        medias = [
            InputMediaPhoto(botfunc.gef_foto(call.data)[0]),
            InputMediaPhoto(botfunc.gef_foto(call.data)[1]),
            InputMediaPhoto(botfunc.gef_foto(call.data)[2])
        ]

        bot.send_media_group(call.from_user.id,medias)
        bot.send_message(call.from_user.id,f'<b>Название:</b> {nameHotel}\n'
                                           f'<b>Адресс: </b> {addressLine}\n'
                                           f'<b>Цена: </b> {price}\n'
                                           f'<b>Сайт: </b> https://www.hotels.com/h{call.data}.Hotel-Information'
                         ,parse_mode='Html')


