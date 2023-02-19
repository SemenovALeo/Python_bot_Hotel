from loader import bot
from states.UserState import UserState
from telebot.types import Message
import utils.botfunc as botfunc



@bot.message_handler(commands=['lowprice'])
def lowprice(message: Message) -> None:
    bot.set_state(message.from_user.id, UserState.city, message.chat.id)
    bot.send_message(message.from_user.id, f'В каком городе будем искать?')
    print(message.from_user.language_code)

@bot.message_handler(state=UserState.city)
def get_city(message: Message) -> None:
    if message.text.isalpha():
        bot.send_message(message.from_user.id, f'Сколько отелей показываем? (не больше 10)')
        bot.set_state(message.from_user.id, UserState.number_of_hotels)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['city'] = message.text
            data['language'] = message.from_user.language_code + '_' + message.from_user.language_code.upper()
            data['id_city'] = botfunc.get_id_region(message.text)
    else:
        bot.send_message(message.from_user.id, 'Название города может содержать только буквы')

@bot.message_handler(state=UserState.number_of_hotels)
def checkInDate(message: Message) -> None:
    bot.send_message(message.from_user.id, f'Введите дату заезда в формате mm/dd/yyyy')
    bot.set_state(message.from_user.id, UserState.checkInDate)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['quantity_hotel'] = message.text


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
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['adults'] = message.text
        botfunc.get_hotel(data)
    botfunc.get_hotel(data)

