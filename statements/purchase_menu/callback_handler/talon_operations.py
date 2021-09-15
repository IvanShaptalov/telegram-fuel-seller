import json

import telebot
from icecream import ic
from telebot.types import PhotoSize

import commands
import config_interpreter
import main
from statements import useful_methods
from utils import db_util, api_util, key_util


# solved test part
def save_gas_type(call, bot: telebot.TeleBot):
    if call.data:
        db_util.write_obj_to_table(table_class=db_util.TalonStatement,
                                   identifier=db_util.TalonStatement.statement_talon_id,
                                   value=1,
                                   talon_statement=call.data)
        bot.send_message(chat_id=call.message.chat.id,
                         text='Вы выбрали: {}'.format(call.data),
                         reply_markup=key_util.remove_keyboard())


def select_gas_type(message, bot: telebot.TeleBot):
    # solved select gas type
    chat_id = useful_methods.id_from_message(message)
    api_util.get_blank_and_refresh_data()
    fuel_list = json.loads(api_util.get_fuel_info_from_db().fuel_info_json)
    # this moment
    # result = {fuel['fuel_type']['fuel_type']: "{} - {}".format(fuel['fuel_type']['fuel_type'], fuel['fuel_type']['fuel_type_id']) for fuel in fuel_list}
    unique_fuel_type = list({fuel['fuel_type']['fuel_type']: {
        fuel['fuel_type']['fuel_type']: fuel['fuel_type']['fuel_type']} for fuel in
                                fuel_list}.values())
    print(unique_fuel_type)
    markup = key_util.create_inline_keyboard(callback_data=True, title_to_data=unique_fuel_type)
    bot.send_message(chat_id=chat_id,
                     text='Выберите тип талона для загрузки',
                     reply_markup=markup)


def talon_loader(message, bot: telebot.TeleBot):
    talon_statement = db_util.get_from_db_eq_filter_not_editing(table_class=db_util.TalonStatement,
                                                                identifier=db_util.TalonStatement.statement_talon_id,
                                                                value=1)
    chat_id = useful_methods.id_from_message(message)

    if isinstance(talon_statement, db_util.TalonStatement):
        gas_type = talon_statement.talon_statement
        photo = message.photo[-1]
        assert isinstance(photo, PhotoSize)
        photo_file_id = photo.file_id
        photo_unique_file_id = photo.file_unique_id
        message_id = message.id
        # if photo not exist, save them
        if not check_unique(photo_unique_file_id):
            db_util.write_obj_to_table(table_class=db_util.TalonInfo,
                                       identifier=db_util.TalonInfo.photo_unique_file_id,
                                       value=photo_unique_file_id,
                                       photo_unique_file_id=photo_unique_file_id,
                                       gas_type=gas_type,
                                       photo_file_id=photo_file_id,
                                       message_id=message_id)

            ic('saved')
        else:
            # noinspection PyBroadException
            try:
                ic('already exists!')
                bot.delete_message(chat_id=config_interpreter.talon_group_chat,
                                   message_id=message_id)
            except:
                ...
    else:
        bot.send_message(chat_id=chat_id,
                         text='Выберите тип топлива:\n'
                              '{}'.format(commands.select_gas_type))


def check_unique(photo_unique_file_id):
    info = db_util.get_from_db_eq_filter_not_editing(table_class=db_util.TalonInfo,
                                                     identifier=db_util.TalonInfo.photo_unique_file_id,
                                                     value=photo_unique_file_id)
    if isinstance(info, db_util.TalonInfo):
        return True
    return False


def send_tokens(json_data):
    ic('send tokens menu')
    data = json.loads(json_data)
    bot = main.bot
    # solved send in token count and make talons expired
    pre_info = db_util.get_from_db_eq_filter_not_editing(table_class=db_util.TalonInfo,
                                                         identifier=db_util.TalonInfo.expired,
                                                         value=False,
                                                         get_type='many')
    talon_type = data['fuel_type']
    info = None
    # solved check this moment
    for inf in pre_info:
        if isinstance(inf, db_util.TalonInfo):
            if inf.gas_type == talon_type and not inf.expired:
                info = inf
                break

    # solved send current count tokens
    if isinstance(info, db_util.TalonInfo):
        try:
            bot.send_photo(chat_id=data['client_id'],
                           photo=info.photo_file_id,  # file id!!!not unique file
                           caption=data['text'])
            print(data)
            db_util.edit_obj_in_table(table_class=db_util.TalonInfo,
                                      identifier=db_util.TalonInfo.talon_id,
                                      value=info.talon_id,
                                      expired=True)
        except Exception as e:
            print(e)
            return False
        return True
    return False
