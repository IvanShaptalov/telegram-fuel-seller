import threading
import time
import telebot
from icecream import ic

import commands
import config_interpreter
import local_server
from statements import statement_switcher
from statements.purchase_menu.callback_handler import buy_fuel_callback, talon_operations
from utils import db_util

error_count = 0


def start_polling():
    ic('bot started')
    db_util.create_db()
    ic('db created (if not exist)')
    global error_count
    try:
        bot.polling()
    except Exception as error:
        print(error)
        time.sleep(5)
        ic(error_count)
        error_count += 1
        if error_count > 5:
            print('end')
            return
        start_polling()


bot = telebot.TeleBot(config_interpreter.BOT_TOKEN)


def start_bot_work():
    # text handling (just message,text)
    # user not blocked bot
    @bot.message_handler(content_types=['photo'])
    def check_file_id(message):
        print(message)
        if message.chat.id == config_interpreter.talon_group_chat:
            ic('handle talon')
            # solved check this part
            talon_operations.talon_loader(message, bot)
        else:
            buy_fuel_callback.handle_screenshot(message, bot)
            ic('handle screenshot')

    @bot.message_handler(content_types=['text', 'photo'])
    def answer(message):

        if isinstance(message, telebot.types.Message):
            # load talons
            print(message.chat.id)
            if commands.select_gas_type in message.text and message.chat.id == config_interpreter.talon_group_chat:
                talon_operations.select_gas_type(message, bot)

                return
            # select current user statement
            user_st_m = db_util.from_db_get_statement(message.chat.id, message.text, message.from_user.first_name)

            # select func to call
            func_message = statement_switcher.select_statement_message(user_st_m)

            # create client cabinet if not exist

            ic(user_st_m, func_message)
            # in argument : [message|callback], bot only, call function
            if func_message:
                func_message(message=message, bot=bot)

    @bot.callback_query_handler(func=lambda call: True)
    def callback_answer(call):

        user_st_c = None
        if call.message:
            message = call.message
            if message.chat.id == config_interpreter.talon_group_chat:
                talon_operations.save_gas_type(call, bot)
                return
            user_st_c = db_util.from_db_get_statement(message.chat.id, message.text, message.from_user.first_name)
        elif call.from_user:
            user_st_c = db_util.from_db_get_statement(call.from_user.id, commands.start_menu, call.from_user.first_name)

        if user_st_c:
            func_callback = statement_switcher.select_statement_callback(user_st_c)
            ic(user_st_c, func_callback)
            # in argument : [message|callback], bot only
            if func_callback:
                func_callback(call=call, bot=bot)

    @bot.message_handler(content_types=['contact'])
    def contact_answer(contact):
        ic('handle contact')
        buy_fuel_callback.handle_contact(contact, bot)

    start_polling()


if __name__ == '__main__':
    # thread = threading.Thread(target=start_event, args=[])
    # thread.start()
    db_util.create_db()
    thread = threading.Thread(target=local_server.run_listener)
    thread.start()
    start_bot_work()
