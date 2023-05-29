from environs import Env
import telebot
from telebot import types
from telebot.util import quick_markup


Env().read_env()
token = Env().str('TG_BOT_TOKEN')
agreement = Env().str('AGREEMENT')
bot = telebot.TeleBot(token)

# empty
chats = {}


# buttons
number = types.KeyboardButton(text='Позвонить')
enroll = types.KeyboardButton(text='Записаться')
info = types.KeyboardButton(text='О нас')
choose_salon = types.KeyboardButton(text='Выбрать салон')
choose_master = types.KeyboardButton(text='Выбрать мастера')
accept = types.KeyboardButton(text='Подтвердить')
back = types.KeyboardButton(text='Назад')
skip = types.KeyboardButton(text='Пропустить')
pay = types.KeyboardButton(text='Оплатить')
cancel = types.KeyboardButton(text='Отменить')


# markups
markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
markup_menu.add(info, number, enroll)

markup_choose = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
markup_choose.add(choose_master, choose_salon, number)

markup_accept = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
markup_accept.add(accept, cancel)

markup_pay = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
markup_pay.add(pay, skip)

markup_skip = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
markup_skip.add(skip)

# quick markup
client_markup = quick_markup({
    'О нас': {'callback_data': 'get_info'},
    'Записаться': {'callback_data': 'order'},
    'Позвонить': {'callback_data': 'number'},
})


# TODO rename this file
