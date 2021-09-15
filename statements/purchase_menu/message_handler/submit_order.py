import telebot

import commands
import config_interpreter
from statements import useful_methods
from utils import key_util, save_sign_util, api_util


def handle_message(message: telebot.types.Message, bot: telebot.TeleBot):
    chat_id = useful_methods.id_from_message(message)

    if message.text == commands.submit_order:
        try:
            api_util.send_sign_request(chat_id=chat_id)
        except Exception as e:
            print('request not send\ntype - {}'.format(type(e), e))
            bot.send_message(chat_id=chat_id,
                             text='К сожалению ваш заказ не подтвержден\nОбратная связь: {}!'.format(config_interpreter.back_ref),
                             reply_markup=key_util.remove_keyboard())
        else:
            bot.send_message(chat_id=chat_id,
                             text='Ваш заказ успешно подтвержден!',
                             reply_markup=key_util.remove_keyboard())
