"""choose profile - first statement in bot,
(you can choose admin account if your account exists in admin_accounts db)"""
import telebot

import commands
from statements import useful_methods
from utils import db_util, key_util, description_text

sub_commands = [
    'как заказать топливо?',
    'сроки действия талонов',
    'как пользоватся',
    'как купить талон?',
    'обратная связь',
]


def handle_message(message: telebot.types.Message, bot: telebot.TeleBot):
    chat_id = useful_methods.id_from_message(message)
    if message.text == commands.description_menu:
        markup = key_util.create_reply_keyboard(sub_commands)
        bot.send_message(chat_id=chat_id,
                         text='Выберите пункт из списка:',
                         reply_markup=markup)
    elif message.text in sub_commands:
        bot.send_message(chat_id=chat_id,
                         text=get_description_answer(message.text))
    else:
        bot.send_message(chat_id=chat_id,
                         text='Выберите ')


def get_description_answer(text):
    answer = 'выберите пункт из списка:'
    if text == sub_commands[0]:
        answer = description_text.buy_fuel

    elif text == sub_commands[1]:
        answer = description_text.expire_talon

    elif text == sub_commands[2]:
        answer = description_text.use_talon

    elif text == sub_commands[3]:
        answer = 'для покупки топлива откройте меню КУПИТЬ ТОПЛИВО \n Затем следуйте указанным иструкциям'

    elif text == sub_commands[4]:
        answer = 'перейдите по ссылке: \n @demeingggdf'

    return answer
