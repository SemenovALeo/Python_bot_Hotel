from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def hotel_markup(data):
    destinations = InlineKeyboardMarkup()

    for value in data['hotels']:
        destinations.add(InlineKeyboardButton(text=value['name'], callback_data= int(value['id'])))
    return destinations
