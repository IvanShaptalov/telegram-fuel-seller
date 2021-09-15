import datetime
import json
import requests
from icecream import ic

import config_interpreter
from utils import db_util


# todo create tests get_from_db, get_from_server, get without connection, get without db, get without db and connection - 5 tests

def get_data_from_server():
    # fixme after creating change host
    link = 'http://{}/api/get_fuel/{}?format=json'.format(config_interpreter.server_host,
                                                          config_interpreter.server_token)
    data = requests.get(link)
    return data.text


def get_card_from_server():
    # todonow create test and safe this part
    print('get_card')
    link = 'http://{}/api/get_card/{}?format=json'.format(config_interpreter.server_host,
                                                          config_interpreter.server_token)
    data = requests.get(link)
    result = json.loads(data.text)['card']
    return result


def prepare_fuel_list_to_blank(fuel_list):
    result_fuel_list = []

    unique_fuel_type = set([fuel['fuel_type']['fuel_type'] for fuel in fuel_list])

    for fuel_type in unique_fuel_type:
        result_fuel_list.append('\n<u><b>Тип топлива: {} </b></u>\n'.format(fuel_type))
        for fuel in fuel_list:
            if fuel:
                price = fuel['fuel_price']
                count = fuel['fuel_count']
                current_fuel_type = fuel['fuel_type']['fuel_type']
                if fuel_type == current_fuel_type:
                    blank = "* количество: <i>{}</i> л. цена: <i>{}</i> грн".format(count, price)
                    result_fuel_list.append(blank)

    fuel_blank = ''.join(['\t{} {}'.format(el, '\n') for el in result_fuel_list])
    return fuel_blank


def create_blank_and_save_in_db():
    # try get data from server and convert to list from json
    try:
        json_list = get_data_from_server()
        fuel_list = json.loads(json_list)
    except Exception as e:
        # if server not responding get from db
        print(e)
        'error with server'
        fuel = get_fuel_info_from_db(connection_lost=True)
        if isinstance(fuel, db_util.Fuel):
            fuel_blank = fuel.blank
        else:
            fuel_blank = fuel
    else:
        # if all ok - get info from server and save in database
        fuel_blank = prepare_fuel_list_to_blank(fuel_list)
        save_to_db(fuel_blank, json_list)
    return fuel_blank


def save_to_db(fuel_blank, json_list):
    db_util.write_obj_to_table(table_class=db_util.Fuel,
                               identifier=db_util.Fuel.fuel_blank_id,
                               value=1,
                               fuel_blank_id=1,
                               fuel_info_json=json_list,
                               blank=fuel_blank,
                               last_update=datetime.datetime.now())
    print('saved')


# region blank db


def data_is_deprecated():
    # try get fuel

    fuel = db_util.get_from_db_eq_filter_not_editing(table_class=db_util.Fuel,
                                                     identifier=db_util.Fuel.fuel_blank_id,
                                                     value=1)
    # if fuel exists check deprecation on way subtraction date now and date from db
    # fixme when deploy on server data will be different
    if isinstance(fuel, db_util.Fuel):
        ic('data: ')
        time_difference = datetime.datetime.now() - fuel.last_update
        print(time_difference.seconds)
        seconds_to_deprecate = 300
        if time_difference.seconds > seconds_to_deprecate:
            ic('deprecated')
            return True
        else:
            ic('still fresh')
            return False
    # if database don`t have value update info
    else:
        create_blank_and_save_in_db()
        ic('created now')
        return False


def get_fuel_info_from_db(connection_lost=None):
    fuel = db_util.get_from_db_eq_filter_not_editing(table_class=db_util.Fuel,
                                                     identifier=db_util.Fuel.fuel_blank_id,
                                                     value=1)
    # if blank  exists return it
    if isinstance(fuel, db_util.Fuel):
        return fuel
    elif not connection_lost:
        # if blank not exist but connection is not lost try
        # to get it from server
        ic('try get from db but not exist')
        # recursion
        return create_blank_and_save_in_db()
    else:
        # if connection lost -
        return 'На данный момент предложений нет'


# endregion

def get_blank_and_refresh_data():
    # load from server if data deprecated
    if data_is_deprecated():
        ic('from server')
        blank = create_blank_and_save_in_db()
    else:
        # get from db
        ic('from db')
        fuel_or_blank = get_fuel_info_from_db()
        if isinstance(fuel_or_blank, db_util.Fuel):
            blank = fuel_or_blank.blank
        else:
            blank = fuel_or_blank
    return blank


# region post
def send_sign_request(chat_id):
    data = db_util.get_from_db_eq_filter_not_editing(table_class=db_util.ClientSignJson,
                                                     identifier=db_util.ClientSignJson.user_chat_id,
                                                     value=chat_id)

    if isinstance(data, db_util.ClientSignJson):
        json_data = data.all_info_json
        result = json.loads(json_data)
        assert isinstance(result, dict)
        r = requests.post("http://localhost:8000/api/get_new_sign/ahdjf32784238yhdw23342ywfw2jdsofkdfjh", data=result)
        return r

# endregion
