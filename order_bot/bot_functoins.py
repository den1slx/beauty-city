import telebot
from order_bot.other import bot, chats, client_markup


def get_info(message: telebot.types.Message):
    user = chats[message.chat.id]
    info = f'Здесь будет информация о нас.'
    # TODO add info
    bot.send_message(message.chat.id, info, parse_mode='Markdown')
    user['callback'] = None
    user['callback_source'] = []


def create_order(message: telebot.types.Message):
    user = chats[message.chat.id]
    info = 'Здесь будут кнопки '
    # TODO add logic
    bot.send_message(message.chat.id, info)
    user['callback'] = None
    user['callback_source'] = []


def get_number(message: telebot.types.Message):
    user = chats[message.chat.id]
    info = '''
Наш номер: 8-800-555-3535
    Рады звонку в любое время!
    '''
    bot.send_message(message.chat.id, info)
    user['callback'] = None
    user['callback_source'] = []


def show_main_menu(chat_id):
    msg = bot.send_message(chat_id, 'Варианты действий', reply_markup=client_markup)
    chats[chat_id]['callback_source'] = [msg.id, ]
    chats[chat_id]['callback'] = None


def start_bot(message: telebot.types.Message):
    bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.username}.')
    chats[message.chat.id] = {
        'callback': None,  # current callback button
        'agreement': None,  # для согласия на обработку данных
        'callback_source': None,
        # TODO add more keys
    }
    show_main_menu(message.chat.id)
