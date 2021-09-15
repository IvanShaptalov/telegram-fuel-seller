"""choose profile - first statement in bot,
(you can choose admin account if your account exists in admin_accounts db)"""
import telebot
from icecream import ic

import commands
from statements import useful_methods
from utils import key_util, api_util


def handle_message(message: telebot.types.Message, bot: telebot.TeleBot):
    chat_id = useful_methods.id_from_message(message)
    # get info from database or send request to server
    # if message.text == commands.pricelist:
    #     fuel_list = api_util.get_blank_and_refresh_data()
    #     bot.send_message(chat_id=chat_id,
    #                      text=fuel_list,
    #                      parse_mode='html',
    #                      reply_markup=key_util.remove_keyboard())
    bot.send_message(chat_id=chat_id,
                     text='test',
                     reply_markup=key_util.create_reply_keyboard(['Меню']))
    # get unique fuel type
