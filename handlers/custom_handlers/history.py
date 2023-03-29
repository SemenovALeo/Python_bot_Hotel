from loader import bot
from states.UserState import User_State
from telebot.types import Message
from database.models import Order
from database.models import User
from database.models import Extradition

@bot.message_handler(commands=['history'])
def history(message: Message) -> None:
    bot.set_state(message.from_user.id, User_State.history, message.chat.id)
    user = User.get(user_id = message.from_user.id)
    orders = [x for x in Order.select().where(Order.user_id == user) ]
    extraditions = [x for x in Order.select().where(Order.id == Extradition.id) ]
    for order, extradition in orders, extraditions:
            bot.send_message(message.from_user.id, f' Добрый день {user.username} ! Ты сегодня {order.created_date} делал запрос в город {order.city}'
                                               f' c {order.check_in} по {order.check_out} на {order.adults} персоны {extraditions.name}', parse_mode='Html')
