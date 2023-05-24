import telebot
from order_bot.other import bot, chats, client_markup, markup_choose, markup_dt


def get_info(message: telebot.types.Message):
    user = chats[message.chat.id]
    info = f'Здесь будет информация о нас.'
    # TODO add info
    bot.send_message(message.chat.id, info, parse_mode='Markdown')
    user['callback'] = None


def create_order(message: telebot.types.Message, step=0):
    user = chats[message.chat.id]
    if step == 0:
        text = 'Меню:'
        msg = bot.send_message(message.chat.id, text, reply_markup=markup_choose)

        bot.register_next_step_handler(msg, create_order, 1)
    elif step == 1:
        user['text'] = message.text
        if user['text'] == 'Позвонить':
            get_number(message)
            return
        elif user['text'] == 'Выбрать салон':
            user['type'] = 'салон'
        elif user['text'] == 'Выбрать мастера':
            user['type'] = 'мастер'
        else:
            user['callback'] = None
            return

        msg = bot.send_message(message.chat.id, user['text'], reply_markup=markup_dt)  # TODO change markup for step 2
        bot.register_next_step_handler(msg, create_order, 2)
# TODO step2: choose_service
    elif step == 3:
        user['text'] = message.text
        if user['text'] == 'Позвонить':
            get_number(message)

    user['callback'] = None
    # TODO add next steps
    return


def get_number(message: telebot.types.Message):
    user = chats[message.chat.id]
    info = '''
Наш номер: 8-800-555-3535
    Рады звонку в любое время!
    '''
    bot.send_message(message.chat.id, info)
    user['callback'] = None


def show_main_menu(chat_id):
    msg = bot.send_message(chat_id, 'Варианты действий', reply_markup=client_markup)
    chats[chat_id]['callback'] = None


def start_bot(message: telebot.types.Message):
    bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.username}.')
    chats[message.chat.id] = {
        'callback': None,  # current callback button
        'agreement': None,  # для согласия на обработку данных
        'callback_source': None,  # возможно будет удалено
        'text': None,  # текст с кнопки
        'type': None,  # салон или мастер
        'service': None,  # услуга
        # TODO add more keys
    }
    show_main_menu(message.chat.id)
