import telebot
from telebot import types

from order_bot.other import bot, chats, client_markup, markup_choose, \
    number, markup_accept, markup_skip, markup_pay, agreement
from order_bot.db_functions import get_salon_procedure, get_master_procedure, get_salons,\
    get_masters, get_promo, get_decades, update_prepay_status, create_client, get_ids


def get_info(message: telebot.types.Message):
    user = chats[message.chat.id]
    info = f'Здесь будет информация о нас.'
    # TODO add info
    bot.send_message(message.chat.id, info, parse_mode='Markdown')
    user['callback'] = None


def card_pay(num, date, cvc):
    #  TODO use card_data for pay

    return False  # return True if transaction verified


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
            salons = get_salons()
            markup_salons = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup_salons.add(number)
            for salon in salons:
                markup_salons.add(types.KeyboardButton(salon['address']))
            msg = bot.send_message(message.chat.id, 'Салоны:', reply_markup=markup_salons)
            bot.register_next_step_handler(msg, create_order, 2)
        elif user['text'] == 'Выбрать мастера':
            user['type'] = 'мастер'
            masters = get_masters()
            markup_masters = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup_masters.add(number)
            for master in masters:
                markup_masters.add(types.KeyboardButton(master['name']))
            msg = bot.send_message(message.chat.id, masters, reply_markup=markup_masters)
            bot.register_next_step_handler(msg, create_order, 2)
        else:
            user['callback'] = None
            return
    elif step == 2:  # choose service
        user['text'] = message.text
        if user['text'] == 'Позвонить':
            get_number(message)
            return
        if user['type'] == 'салон':
            user['salon'] = message.text
            services = get_salon_procedure(message.text)
        else:
            user['master'] = message.text
            services = get_master_procedure(message.text)
        markup_services = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup_services.add(number)
        text = f"Предоставляемые услуги:{user['master']}"
        for service in services:
            markup_services.add(types.KeyboardButton(service['title']))
            text += f"\n {service['title']}. Цена: {service['price']}"
        msg = bot.send_message(message.chat.id, text, reply_markup=markup_services)
        bot.register_next_step_handler(msg, create_order, 3)
        return

    elif step == 3:  # choose decade
        user['service'] = message.text
        text = f'Выберите числа'
        if message.text == 'Позвонить':
            get_number(message)
            return
        decades = get_decades()
        markup_decades = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup_decades.add(number)
        for decade in decades:
            markup_decades.add(types.KeyboardButton(text=f"{decade['decade']}"))
        msg = bot.send_message(message.chat.id, text, reply_markup=markup_decades)
        bot.register_next_step_handler(msg, create_order, 4)
    elif step == 4:  # choose day
        user['text'] = message.text
        if user['text'] == 'Позвонить':
            get_number(message)
            return
        text = 'Выберите день'
        days = [{'time': 1}, {'time': 2}, {'time': 3}]  # TODO add data from db
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
        user['date'] = message.text  # TODO str to datetime. used in step==14
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
        user['name'] = message.text
        msg = bot.send_message(
            message.chat.id,
            'Соглашение на обработку персональных данных:',
            reply_markup=markup_accept
        )
        bot.send_document(message.chat.id, open(agreement, 'rb'))
        bot.register_next_step_handler(msg, create_order, 8)
    elif step == 8:
        if message.text == 'Отменить':
            clean_user(user)
            get_info(message)
            return
        text = 'Введите промокод'
        msg = bot.send_message(message.chat.id, text, reply_markup=markup_skip)
        bot.register_next_step_handler(msg, create_order, 9)
    elif step == 9:
        if message.text != 'Пропустить':
            user['promo'] = get_promo(message.text)
        salon_id, master_id, service_id = get_ids(user['salon'], user['master'], user['service'])
        create_client(user['date'], salon_id, user['name'], user['phone_number'], master_id, service_id, False)
        text = 'Запись прошла успешно. Желаете оплатить сразу?'
        msg = bot.send_message(message.chat.id, text, reply_markup=markup_pay)
        bot.register_next_step_handler(msg, create_order, 10)
    elif step == 10:
        text = 'введите номер карты'
        msg = bot.send_message(message.chat.id, text)
        bot.register_next_step_handler(msg, create_order, 11)
    elif step == 11:
        user['card_num'] = message.text
        text = 'введите трехзначный номер карты'
        msg = bot.send_message(message.chat.id, text)
        bot.register_next_step_handler(msg, create_order, 12)
    elif step == 12:
        user['cvc'] = message.text
        text = 'введите дату в формате MM/YY'
        msg = bot.send_message(message.chat.id, text)
        bot.register_next_step_handler(msg, create_order, 13)
    elif step == 13:
        user['card_date'] = message.text
        text = f"""Ваша карта: {user['date']}
        Номер: {user['card_num']}
        Дата:{user['card_date']}
        cvc: {user['cvc']}
        """
        msg = bot.send_message(message.chat.id, text, reply_markup=markup_pay)
        bot.register_next_step_handler(msg, create_order, 14)
    elif step == 14:
        pay_status = card_pay(user['card_num'], user['card_date'], user['cvc'])
        if pay_status:
            text = 'Оплата прошла успешно'
        else:
            text = 'Оплата не удалась'
        if message.text == 'Оплатить':
            # TODO add pay form
            date = ''
            update_prepay_status(name=user['name'], phone=user['phone_number'], date=user['date'], status=True)
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
    show_main_menu(message.chat.id)


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
        'pay': None,
        'date': None,
        'master': None,
        'salon': None,
        'cvc': None,
        'card_date': None,
        'card_num': None,

        # TODO add more keys to clean
    })


def start_bot(message: telebot.types.Message):
    bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.username}.')
    chats[message.chat.id] = {
        'callback': None,
        'agreement': None,
        'text': None,
        'type': None,
        'service': None,
        'phone_number': None,
        'name': None,
        'promo': None,
        'pay': None,
        'date': None,
        'master': None,
        'salon': None,
        'cvc': None,
        'card_date': None,
        'card_num': None,
    }
    show_main_menu(message.chat.id)
