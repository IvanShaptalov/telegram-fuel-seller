"""choose profile - first statement in bot,
(you can choose admin account if your account exists in admin_accounts db)"""
import json

import telebot

import commands
from statements import useful_methods
from utils import key_util, api_util


def handle_message(message: telebot.types.Message, bot: telebot.TeleBot):
    chat_id = useful_methods.id_from_message(message)

    if message.text == commands.buy_fuel:
        api_util.get_blank_and_refresh_data()
        fuel_list = json.loads(api_util.get_fuel_info_from_db().fuel_info_json)
        unique_fuel_type = list({fuel['fuel_type']['fuel_type']: {
            fuel['fuel_type']['fuel_type']: change_value(fuel['fuel_type']['fuel_type_id'])} for fuel in
                                 fuel_list}.values())
        print(unique_fuel_type)
        markup = key_util.create_inline_keyboard(callback_data=True, title_to_data=unique_fuel_type)
        bot.send_message(chat_id=chat_id,
                         text='Выберите тип топлива',
                         reply_markup=markup)
    else:
        try:
            bot.delete_message(message.chat.id, message.id)
        except Exception:
            ...
        bot.send_message(chat_id=chat_id,
                         text='следуйте указанным инструкциям')


def change_value(fuel_type_id):
    return "{}{}".format(key_util.select_fuel_mark, fuel_type_id)
