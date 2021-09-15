import datetime
import json
import random

import telebot

import commands
import config_interpreter
from statements import useful_methods
from utils import api_util, db_util, key_util, save_sign_util
from utils.key_util import select_fuel_mark, select_liter_mark


# noinspection PyBroadException
def handle_callback(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    print(call)
    chat_id = useful_methods.id_from_message(call.message)
    api_util.get_blank_and_refresh_data()
    fuel_info = api_util.get_fuel_info_from_db()
    # region fuel selected
    if select_fuel_mark in call.data:
        print('select fuel')
        liter_info, liter_message = current_fuel_liter_info(fuel_info, call)
        markup = key_util.create_inline_keyboard(callback_data=True, title_to_data=liter_info)
        bot.send_message(chat_id=chat_id,
                         text=liter_message,
                         reply_markup=markup or None)
        try:
            bot.delete_message(chat_id, call.message.id)
        except:
            ...

    # endregion

    # region liter selected
    if select_liter_mark in call.data:
        print(useful_methods.replace_call_data(call).data)
        fuel_id = call.data
        fuel_list = json.loads(fuel_info.fuel_info_json)

        current_fuel = None
        for fuel in fuel_list:
            if fuel['fuel_id'] == int(fuel_id):
                current_fuel = fuel
                break
        if current_fuel:
            text = 'Счет:\nВы  выбрали: ' + call.message.text.split(':')[
                0] + ' {} л\nЦена - {}.\nВернутся к выбору топлива: {}'.format(current_fuel['fuel_count'],
                                                                               current_fuel['fuel_price'],
                                                                               commands.buy_fuel)
            try:
                bot.delete_message(chat_id, call.message.id)
            except:
                ...
            bot.send_message(chat_id=chat_id,
                             text=text)

            save_sign_util.save_parameter(chat_id=chat_id,
                                          fuel_id=current_fuel['fuel_id'])
            # solved enter phone number
            markup = key_util.create_request_markup(title='Поделиться номером телефона', request_contact=True)
            bot.send_message(chat_id=chat_id,
                             text='Чтобы совершить покупку нажмите на кнопку \'Поделится номером телефона\'',
                             reply_markup=markup)

    # endregion


def current_fuel_liter_info(fuel_info, call):
    if isinstance(fuel_info, db_util.Fuel):
        liter_list = []
        fuel_type_id = useful_methods.replace_call_data(call).data
        current_fuel_type_title = 'На данный момент этого топлива нет в наличии '
        fuel_dict = json.loads(fuel_info.fuel_info_json)
        for fuel in fuel_dict:
            if fuel['fuel_type']['fuel_type_id'] == int(fuel_type_id):
                liter_list.append(
                    {'{} л.'.format(fuel['fuel_count']): '{}{}'.format(select_liter_mark, fuel['fuel_id'])})
                current_fuel_type_title = '{}: выбрать количество\nменю выбора: {}'.format(
                    fuel['fuel_type']['fuel_type'], commands.buy_fuel)

        return liter_list, current_fuel_type_title


def handle_contact(update: telebot.types.Message, bot: telebot.TeleBot):
    if update and update.from_user:
        chat_id = useful_methods.id_from_user(update.from_user)
        if update.contact:
            waiting_status = 1
            date = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
            print(date)
            # region save info
            save_sign_util.save_parameter(chat_id=chat_id,
                                          client_phone_number=update.contact.phone_number,
                                          first_last_name="{} {} {}".format(update.from_user.first_name or "",
                                                                            update.from_user.last_name or "",
                                                                            update.from_user.username or ""),
                                          client_id=chat_id,
                                          source_type=config_interpreter.source_type,
                                          sign_date=date,
                                          status_id=waiting_status,
                                          sign_code=random.randint(111111, 999999),
                                          screenshot_link='@link')
            # endregion
            sign = db_util.get_from_db_eq_filter_not_editing(table_class=db_util.ClientSignJson,
                                                             identifier=db_util.ClientSignJson.user_chat_id,
                                                             value=chat_id)

            # region send screenshot
        bot.send_message(chat_id=chat_id,
                         text='Отправьте сумму указанную в счете на данную карту и скиньте скриншот оплаты',
                         reply_markup=key_util.remove_keyboard())
        bot.send_message(chat_id=chat_id,
                         text=api_util.get_card_from_server())
        # endregion
        # save main info
        # solved create screenshot condition , send screenshot to group, send info to server with screenshot link
        # todonow send answer from server with accept or decline, send talon to user


# noinspection PyBroadException
def handle_screenshot(message: telebot.types.Message, bot: telebot.TeleBot):
    chat_id = useful_methods.id_from_message(message)

    photo = message.photo[-1]
    photo_file_id = photo.file_id
    user = message.from_user
    num = random.randint(111111, 999999)
    link = "{} \n #num{} \n{} {} {}".format(config_interpreter.screenshot_group_link, num, user.first_name or "",
                                            user.last_name or "",
                                            "{}".format(user.username) or "")
    bot.send_photo(photo=photo_file_id,
                   caption=link,
                   chat_id=config_interpreter.screenshot_group_chat)
    try:
        bot.delete_message(chat_id, message.id)
    except:
        ...
    save_sign_util.save_parameter(chat_id=chat_id,
                                  screenshot_link=link)
    print('saved')
    bot.send_message(chat_id=chat_id,
                     text='Подтвердите заказ нажав на кнопку \'подтвердить заказ\'',
                     reply_markup=key_util.create_request_markup('подтвердить заказ'))
    return link
