import constant
from statements.main_info.message_handler import description
from statements.pricelist.message_handler import pricelist
from statements.purchase_menu.message_handler import buy_fuel, submit_order
from statements.purchase_menu.callback_handler import buy_fuel_callback
from statements.start_menu import start_menu
from statements.start_menu.message_handler import main_menu


def select_statement_message(statement):
    switcher = {
        # region message handlers
        constant.PriceListMenu.PRICELIST: pricelist.handle_message,
        constant.InfoMenu.DESCRIPTION_MENU: description.handle_message,
        constant.PurchaseMenu.BUY_FUEL: buy_fuel.handle_message,
        constant.StartMenu.MENU: main_menu.handle_message,
        constant.PurchaseMenu.SUBMIT_ORDER: submit_order.handle_message,
        # endregion message handlers
    }
    try:
        message_func = switcher.get(statement)
        return message_func
    except AttributeError:
        message_func = switcher.get('default value')
        return message_func


def select_statement_callback(statement):
    switcher = {
        # region callback handlers

        constant.PurchaseMenu.BUY_FUEL: buy_fuel_callback.handle_callback,
        # endregion callback handlers
    }
    try:
        message_func = switcher.get(statement)
        return message_func
    except AttributeError:
        message_func = switcher.get('default value')
        return message_func
