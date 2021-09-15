"""choose profile - first statement in bot,
(you can choose admin account if your account exists in admin_accounts db)"""
import telebot

import commands
from statements import useful_methods
from utils import db_util, key_util


def handle_message(message: telebot.types.Message, bot: telebot.TeleBot):
    chat_id = useful_methods.id_from_message(message)

    bot.send_message(chat_id=chat_id,
                     text='Выбери опцию')
