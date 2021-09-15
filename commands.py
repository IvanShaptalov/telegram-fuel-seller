import constant

# region commands
start_menu = '/start'
pricelist = '/pricelist'
description_menu = '/description'

buy_fuel = '/buy_fuel'
menu = '/menu'
select_gas_type = '/select_gas_type'

# 1 solved pricelist
# 2 solved bot info
# 3 solved fuel buying
#  3.1 solved create buy menu
#  3.2 solved create talon group
#  3.3 solved send screen to group with link
#  3.4 solved create screenshot group
#  3.5 solved send to server
#  3.6 solved send answer from server
#  3.7 solved answer to user (optional) get talon from talon group
submit_order = 'подтвердить заказ'


# endregion commands
# add command -> add statement -> add command-statement -> sStatement switcher -> add function


def select_statement_via_present_command(command_present):
    switcher = {
        # client
        start_menu: constant.StartMenu.START_MENU,
        pricelist: constant.PriceListMenu.PRICELIST,
        description_menu: constant.InfoMenu.DESCRIPTION_MENU,
        buy_fuel: constant.PurchaseMenu.BUY_FUEL,
        menu: constant.StartMenu.MENU,
        submit_order: constant.PurchaseMenu.SUBMIT_ORDER,
        # end command to constant

    }
    return switcher.get(command_present)


