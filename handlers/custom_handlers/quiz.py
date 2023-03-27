from keyboards.inline.hotel import hotel_markup
from loader import bot
from states.UserState import User_State
from telebot.types import Message
import utils.botfunc as botfunc
from api import api
from database import models

@bot.message_handler(commands=['highprice', 'bestdeal', 'lowprice'])
def lowprice(message: Message) -> None:
    bot.set_state(message.from_user.id, User_State.city, message.chat.id)
    bot.send_message(message.from_user.id, f'В каком городе будем искать?')
    with bot.retrieve_data(message.from_user.id) as data:
        data['command'] = message.text


@bot.message_handler(state=User_State.city)
def get_city(message: Message) -> None:
        bot.send_message(message.from_user.id, f'Сколько отелей показываем? (не больше 10)')
        bot.set_state(message.from_user.id, User_State.number_of_hotels)

        with bot.retrieve_data(message.from_user.id) as data:
            data['city'] = message.text
            data['language'] = message.from_user.language_code + '_' + message.from_user.language_code.upper()


@bot.message_handler(state=User_State.number_of_hotels)
def check_In_Date(message: Message) -> None:

    bot.send_message(message.from_user.id, f'Введите дату заезда в формате dd/mm/yy')
    bot.set_state(message.from_user.id, User_State.checkInDate)

    with bot.retrieve_data(message.from_user.id) as data:
        data['quantity_hotel'] = message.text


@bot.message_handler(state=User_State.checkInDate)
def check_Out_Date(message: Message) -> None:
    bot.send_message(message.from_user.id, f'Введите дату выезда в формате dd/mm/yy')
    bot.set_state(message.from_user.id, User_State.checkOutDate)

    with bot.retrieve_data(message.from_user.id) as data:
        data['check_in'] = botfunc.get_datetime_str(message.text)


@bot.message_handler(state=User_State.checkOutDate)
def get_adults(message: Message) -> None:
    bot.send_message(message.from_user.id, f'Введите количество взрослых')
    bot.set_state(message.from_user.id, User_State.adults)

    with bot.retrieve_data(message.from_user.id) as data:
        data['check_out'] = botfunc.get_datetime_str(message.text)


@bot.message_handler(state=User_State.adults)
def get_adults(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id) as data:
        data['adults'] = message.text
        data['gaiaId'] = api.api_request('locations/v3/search',data,'GET')['sr'][0]['gaiaId']
        data['hotels'] = botfunc.get_hotels(data)
        bot.send_message(message.from_user.id, f'Выберите отель из списка', reply_markup=hotel_markup(data))
