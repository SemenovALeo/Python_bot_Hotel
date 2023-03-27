from loader import bot
from states.UserState import User_State
from telebot.types import Message
from database.models import Order
from database.models import User

@bot.message_handler(commands=['history'])
def history(message: Message) -> None:
    bot.set_state(message.from_user.id, User_State.history, message.chat.id)
    user = User.get(user_id = message.from_user.id)
    orders = [x for x in Order.select().where(Order.user_id == user) ]
    for order in orders:
        bot.send_message(message.from_user.id, f' Добрый день {user.username} ! Ты сегодня {user.created_date} делал запрос в город {user.city}'
                                               f' c {user.check_in} по {user.check_out} на {user.adults} персоны.\n'
                                               f'Вот результать {order.name}, адрес {order.address}, сайт для бронирования: {order.website}', parse_mode='Html')

