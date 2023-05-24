from environs import Env
import telebot
from telebot import types
from telebot.util import quick_markup


Env().read_env()
token = Env().str('TG_BOT_TOKEN')
bot = telebot.TeleBot(token)


# empty
chats = {}


# buttons
number = types.KeyboardButton(text='Позвонить')
enroll = types.KeyboardButton(text='Записаться')
info = types.KeyboardButton(text='О нас')
menu = types.KeyboardButton(text='В меню')
choose_salon = types.KeyboardButton(text='Выбрать салон')
choose_master = types.KeyboardButton(text='Выбрать мастера')
choose_time = types.KeyboardButton(text='Выбрать время')
nearest_time = types.KeyboardButton(text='Ближайшее время')
accept = types.KeyboardButton(text='Подтвердить')
back = types.KeyboardButton(text='Назад')
skip = types.KeyboardButton(text='Пропустить')
pay = types.KeyboardButton(text='Оплатить')


# markups
markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
markup_menu.add(info, number, enroll)

markup_choose = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
markup_choose.add(choose_master, choose_salon, back, number)

markup_dt = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
markup_dt.add(choose_time, menu, back, number)

markup_accept = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
markup_accept.add(accept, menu, back, number)

markup_pay = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
markup_accept.add(pay, skip)


# quick markup
client_markup = quick_markup({
    'О нас': {'callback_data': 'get_info'},
    'Записаться': {'callback_data': 'order'},
    'Позвонить': {'callback_data': 'number'},
})


# TODO rename this file
