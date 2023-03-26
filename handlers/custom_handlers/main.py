from loader import bot
from handlers.custom_handlers.lowprice import low_price
from handlers.custom_handlers.bestdeal import best_deal
from handlers.custom_handlers.highprice import high_price


@bot.callback_query_handler(func=lambda call: True)
def main(call): # <- passes a CallbackQuery type object to your function
    with bot.retrieve_data(call.from_user.id) as data:
        if data['command'] == "/lowprice":
            low_price(call)
        elif data['command'] == "/bestdeal":
            best_deal(call)
        elif data['command'] == "/highprice":
            high_price(call)
