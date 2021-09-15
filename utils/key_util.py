from telebot import types

import commands


def create_request_markup(title, request_contact=None, request_location=None):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
        types.KeyboardButton(text=title, request_contact=request_contact, request_location=request_location))
    return markup


def create_reply_keyboard(*titles, is_resize: bool = True, row_width: int = 1, request_contact=None):
    """@:param args - button titles"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=is_resize, row_width=row_width)
    for title in titles[0]:
        button = types.KeyboardButton(title, request_contact=request_contact)
        markup.add(button)

    return markup


def create_inline_keyboard(switch_inline_query_current_chat=None, callback_data=False,
                           title_to_data=None):
    markup = types.InlineKeyboardMarkup()
    for dictionary in title_to_data:
        for title, data in dictionary.items():
            inline_button = types.InlineKeyboardButton(
                switch_inline_query_current_chat=switch_inline_query_current_chat,
                text=title,
                callback_data=data if callback_data else None)

            markup.add(inline_button, row_width=3)
    return markup


def remove_keyboard():
    markup = types.ReplyKeyboardRemove()
    return markup


select_fuel_mark = 'select_fuel:'
select_liter_mark = 'select_liter:'
inline_marks = [
    select_fuel_mark,
    select_liter_mark,
]
