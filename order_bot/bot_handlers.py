from order_bot.other import telebot, bot
import order_bot.bot_functoins as calls


calls_map = {
    'get_info': calls.get_info,
    'number': calls.get_number,
    'order': calls.create_order,
}


@bot.message_handler(commands=['start'])
def command_menu(message: telebot.types.Message):
    calls.start_bot(message)


@bot.callback_query_handler(func=lambda call: call.data)
def handle_buttons(call):
    calls_map[call.data](call.message)


def run_bot():
    bot.infinity_polling()
