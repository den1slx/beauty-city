import telebot
from order_bot.other import bot, chats, client_markup, markup_choose,\
    number, markup_accept, markup_skip, markup_pay
from telebot import types


def get_info(message: telebot.types.Message):
    user = chats[message.chat.id]
    info = f'Здесь будет информация о нас.'
    # TODO add info
    bot.send_message(message.chat.id, info, parse_mode='Markdown')
    user['callback'] = None


def create_order(message: telebot.types.Message, step=0):
    user = chats[message.chat.id]
    if step == 0:  # main menu
        text = 'Меню:'
        msg = bot.send_message(message.chat.id, text, reply_markup=markup_choose)

        bot.register_next_step_handler(msg, create_order, 1)
    elif step == 1:  # choose salon\master
        user['text'] = message.text
        if user['text'] == 'Позвонить':
            get_number(message)
            return
        elif user['text'] == 'Выбрать салон':
            user['type'] = 'салон'
            salons = [{'address': 'salon_address1'}, {'address': 'salon_address2'}]  # TODO add data from db
            markup_salons = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup_salons.add(number)
            for salon in salons:
                markup_salons.add(types.KeyboardButton(salon['address']))
            msg = bot.send_message(message.chat.id, 'Салоны:', reply_markup=markup_salons)
            bot.register_next_step_handler(msg, create_order, 2)
        elif user['text'] == 'Выбрать мастера':
            user['type'] = 'мастер'
            masters = [{'name': 'master_name1'}, {'name': 'master_name2'}]  # TODO add data from db
            markup_masters = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup_masters.add(number)
            for master in masters:
                markup_masters.add(types.KeyboardButton(master['name']))
            msg = bot.send_message(message.chat.id, 'Мастера:', reply_markup=markup_masters)
            bot.register_next_step_handler(msg, create_order, 2)
        else:
            user['callback'] = None
            return
    elif step == 2:  # choose service
        user['text'] = message.text
        if user['text'] == 'Позвонить':
            get_number(message)
            return
        services = [{'service': 'service1', 'price': '123'},
                    {'service': 'service2', 'price': '456'}]  # TODO add data from db
        markup_services = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup_services.add(number)
        text = 'Предоставляемые услуги:'
        for service in services:
            markup_services.add(types.KeyboardButton(service['service']))
            text += f"\n {service['service']}. Цена: {service['price']}"
        msg = bot.send_message(message.chat.id, text, reply_markup=markup_services)
        bot.register_next_step_handler(msg, create_order, 3)
        return

    elif step == 3:  # choose decade
        user['service'] = message.text
        text = 'Выберите числа'
        if user['text'] == 'Позвонить':
            get_number(message)
            return
        if user['type'] == 'мастер':
            decades = ''  # TODO add data from db
            pass
        elif user['type'] == 'салон':
            decades = ''  # TODO add data from db
            pass
        markup_decades = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup_decades.add(number)
        # temporal data  # TODO delete temporal data
        decades = [{'decade': '1-10', 'month': 'q'},  # get decades from db where status is True
                   {'decade': '11-20', 'month': 'q'},
                   {'decade': '21-31', 'month': 'w'}]
        # end temporal data
        for decade in decades:
            markup_decades.add(types.KeyboardButton(text=f"{decade['decade']}, {decade['month']}"))
        msg = bot.send_message(message.chat.id, text, reply_markup=markup_decades)
        bot.register_next_step_handler(msg, create_order, 4)
    elif step == 4:  # choose day
        user['text'] = message.text
        if user['text'] == 'Позвонить':
            get_number(message)
            return
        text = 'Выберите день'
        decade, month = message.text.split(sep=',')
        days = [{'time': 1}, {'time': 2}, {'time': 3}]  # TODO add data from db. can use decade and month
        markup_days = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup_days.add(number)

        for day in days:
            markup_days.add(types.KeyboardButton(text=f"{day['time']}"))

        msg = bot.send_message(message.chat.id, text, reply_markup=markup_days)
        bot.register_next_step_handler(msg, create_order, 5)
    elif step == 5:
        user['text'] = message.text
        if user['text'] == 'Позвонить':
            get_number(message)
        text = 'Введите номер телефона для связи с вами'
        msg = bot.send_message(message.chat.id, text)
        bot.register_next_step_handler(msg, create_order, 6)
    elif step == 6:
        user['phone_number'] = message.text
        if user['text'] == 'Позвонить':
            get_number(message)
            return
        text = 'Введите ваше имя'
        msg = bot.send_message(message.chat.id, text)
        bot.register_next_step_handler(msg, create_order, 7)
    elif step == 7:
        agreement = get_agreement()
        # bot.send_document(message.chat.id, agreement, reply_markup=markup_accept)  # TODO add agreement document
        msg = bot.send_message(message.chat.id, agreement, reply_markup=markup_accept)
        bot.register_next_step_handler(msg, create_order, 8)
    elif step == 8:
        if message.text == 'Отменить':
            clean_user(user)
            return
        text = 'Введите промокод'
        msg = bot.send_message(message.chat.id, text, reply_markup=markup_skip)
        bot.register_next_step_handler(msg, create_order, 9)
    elif step == 9:
        if message.text != 'Пропустить':
            user['promo'] = message.text  # TODO check promo in promo_codes from db
        # TODO add data to db
        text = 'Запись прошла успешно. Желаете оплатить сразу?'
        msg = bot.send_message(message.chat.id, text, reply_markup=markup_pay)
        bot.register_next_step_handler(msg, create_order, 10)
    elif step == 10:
        text = 'Оплата прошла успешно'
        if message.text == 'Оплатить':
            user['pay'] = True
            # TODO add pay form
            msg = bot.send_message(message.chat.id, text)
        msg = bot.send_message(message.chat.id, 'Оставайтесь с нами')
        clean_user(user)
        return
    return


def get_number(message: telebot.types.Message):
    user = chats[message.chat.id]
    info = '''
Наш номер: 8-800-555-3535
    Рады звонку в любое время!
    '''
    bot.send_message(message.chat.id, info)
    clean_user(user)


def get_agreement():
    agreement = 'Согласие на обработку персональных данных'  # TODO
    return agreement


def show_main_menu(chat_id):
    msg = bot.send_message(chat_id, 'Варианты действий', reply_markup=client_markup)
    chats[chat_id]['callback'] = None


def clean_user(user):
    user.update({
        'callback': None,
        'agreement': None,
        'text': None,
        'type': None,
        'service': None,
        'phone_number': None,
        'name': None,
        'promo': None,
        'pay': None
        # TODO add more keys to clean
    })


def start_bot(message: telebot.types.Message):
    bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.username}.')
    chats[message.chat.id] = {
        'callback': None,  # current callback button
        'agreement': None,  # для согласия на обработку данных
        'text': None,  # отправленный текст
        'type': None,  # салон или мастер
        'service': None,  # услуга
        'phone_number': None,
        'name': None,
        'promo': None,
        'pay': None
        # TODO add more keys for store data for db
    }
    show_main_menu(message.chat.id)
