from loader import bot
from states.UserState import UserState
from telebot.types import Message
import utils.botfunc as botfunc
from api import api


@bot.message_handler(commands=['lowprice'])
def lowprice(message: Message) -> None:
    bot.set_state(message.from_user.id, UserState.city, message.chat.id)
    bot.send_message(message.from_user.id, f'В каком городе будем искать?')



@bot.message_handler(state=UserState.city)
def get_city(message: Message) -> None:
    if message.text.isalpha():
        bot.send_message(message.from_user.id, f'Сколько отелей показываем? (не больше 10)')
        bot.set_state(message.from_user.id, UserState.number_of_hotels)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['city'] = message.text
            data['language'] = message.from_user.language_code + '_' + message.from_user.language_code.upper()
    else:
        bot.send_message(message.from_user.id, 'Название города может содержать только буквы')



@bot.message_handler(state=UserState.number_of_hotels)
def checkInDate(message: Message) -> None:

    bot.send_message(message.from_user.id, f'Введите дату заезда в формате mm/dd/yy')
    bot.set_state(message.from_user.id, UserState.checkInDate)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['quantity_hotel'] = message.text


@bot.message_handler(state=UserState.checkInDate)
def checkOutDate(message: Message) -> None:
    bot.send_message(message.from_user.id, f'Введите дату выезда в формате mm/dd/yy')
    bot.set_state(message.from_user.id, UserState.checkOutDate)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['check_in'] = botfunc.get_datetime_str(message.text)


@bot.message_handler(state=UserState.checkOutDate)
def get_adults(message: Message) -> None:
    bot.send_message(message.from_user.id, f'Введите количество взрозлых')
    bot.set_state(message.from_user.id, UserState.adults)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['check_out'] = botfunc.get_datetime_str(message.text)


@bot.message_handler(state=UserState.adults)
def get_adults(message: Message) -> None:
    bot.send_message(message.from_user.id, f'Введите количество дитей')
    bot.set_state(message.from_user.id, UserState.children)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['adults'] = message.text


@bot.message_handler(state=UserState.children)
def get_adults(message: Message) -> None:
    bot.send_message(message.from_user.id, f'Мы ищем для Вас информацию')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['children'] = message.text
        data['gaiaId']=api.api_request('locations/v3/search',data,'GET')['sr'][0]['gaiaId']
        data['hotels']=api.api_request('properties/v2/list',data,'POST')['data']['propertySearch']['properties']
        botfunc.get_id_region(data)
