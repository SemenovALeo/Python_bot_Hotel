from loader import bot
import utils.botfunc as botfunc


@bot.callback_query_handler(func=lambda call: call.data == 'highprice')
def high_price(call): # <- passes a CallbackQuery type object to your function
    if call.message:
        botfunc.text_output(bot,call)

