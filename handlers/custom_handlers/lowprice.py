import datetime

from loader import bot
from states.UserState import UserState
from telebot.types import Message
import utils.botfunc as botfunc
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from api import api
from datetime import datetime




@bot.message_handler(commands=['lowprice'])
def lowprice(message: Message) -> None:
    bot.set_state(message.from_user.id, UserState.city, message.chat.id)
    bot.send_message(message.from_user.id, f'В каком городе будем искать?')
    # print(message.from_user.language_code)


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

    # bot.send_message(message.from_user.id, f'Введите дату заезда в формате mm/dd/yyyy')
    # bot.set_state(message.from_user.id, UserState.checkInDate)

    calendar, step = DetailedTelegramCalendar(locale='ru').build()
    bot.send_message(message.chat.id,
                     f"Select {LSTEP[step]}",
                     reply_markup=calendar)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['quantity_hotel'] = message.text


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def cal(c):
    result, key, step = DetailedTelegramCalendar(locale='ru', min_date=datetime.now().date()).process(c.data)
    if not result and key:
        bot.edit_message_text(f"Select {LSTEP[step]}",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        # text = f"You selected {result}"
        # bot.send_message(c.message.chat.id,text)
        bot.set_state(c.message.from_user.id, UserState.checkInDate)


@bot.message_handler(state=UserState.checkInDate)
def checkOutDate(message: Message) -> None:
    bot.send_message(message.from_user.id, f'Введите дату выезда в формате mm/dd/yyyy')
    bot.set_state(message.from_user.id, UserState.checkOutDate)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['check_in'] = message.text


@bot.message_handler(state=UserState.checkOutDate)
def get_adults(message: Message) -> None:
    bot.send_message(message.from_user.id, f'Введите количество взрозлых')
    bot.set_state(message.from_user.id, UserState.adults)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['check_out'] = message.text


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
        botfunc.get_id_region(data)