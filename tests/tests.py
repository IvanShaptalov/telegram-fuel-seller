import configparser
import json
import time
import unittest

import requests
import telebot

import config_interpreter
import local_server
import main
from utils import db_util, api_util

json_data = None


class ServerTestCase(unittest.TestCase):
    def test_internet_working(self):
        """test internet connection"""
        url = "https://www.google.com"
        timeout = 5.
        try:
            request = requests.get(url, timeout=timeout)
        except (requests.ConnectionError, requests.Timeout) as exception:
            self.fail("No internet connection.")

    def test_admin_server_work(self):
        global json_data
        link = 'http://{}/api/get_fuel/{}?format=json'.format(config_interpreter.server_host,
                                                              config_interpreter.server_token)
        try:
            data = requests.get(link)
        except Exception as e:
            print(type(e), e)
            self.fail("admin server don't work")
        else:
            json_data = data.text
            return data.text

    def test_json_data_from_server(self):
        global json_data
        if json_data is None:
            self.fail("data is none, server not work")
        data = json.loads(json_data)
        print(data)

    def test_get_card_from_server(self):
        try:
            result = api_util.get_card_from_server()
            print(result)
        except Exception as e:
            self.fail("card not exists")

    def test_local_server_work(self):
        link = 'http://localhost:{}'.format(local_server.PORT)

        try:
            data = requests.get(link, timeout=3)
        except Exception as e:
            print(type(e), e)
            self.fail("local server don't work")
        else:
            return data.text


class DatabaseTestCase(unittest.TestCase):
    def test_db_instances(self):
        one = 1
        target_list = (
            {'cls': db_util.TalonInfo, 'identifier': db_util.TalonInfo.talon_id, 'value': one,
             'msg': "talon not exists"},

            {'cls': db_util.TalonStatement, 'identifier': db_util.TalonStatement.statement_talon_id,
             'value': one, 'msg': "talon not chosen"},

            {'cls': db_util.Fuel, 'identifier': db_util.Fuel.fuel_blank_id, 'value': one,
             'msg': "fuel blank not exists"})

        for target in target_list:
            info = db_util.get_from_db_eq_filter_not_editing(table_class=target['cls'],
                                                             identifier=target['identifier'],
                                                             value=target['value'])
            print(info)
            self.assertIsInstance(info, target['cls'], msg=target['msg'])


class ConfigTestCase(unittest.TestCase):
    def test_config_exists(self):
        config = configparser.ConfigParser()
        config.read(config_interpreter.CONFIG_PATH)
        try:
            BOT_TOKEN = config['Bot']['bot_token']
            alchemy_db_path = config['DataBase']['sql_alchemy_path']
            server_token = config['Server']['token']
            server_host = config['Server']['host']
            source_type = 'telegram'
            talon_group_chat = int(config['GroupChat']['talons'])
            talon_group_link = config['GroupChat']['link_talons']
            screenshot_group_chat = int(config['GroupChat']['screenshots'])
            screenshot_group_link = config['GroupChat']['link_screen']
            back_ref = config['Feedback']['feed']
        except KeyError as e:
            print(e, " in config interpreter")
            self.fail("config file is not correct")


class BotTestCase(unittest.TestCase):
    def test_talon_group(self):
        bot = main.bot
        try:
            message = bot.send_message(chat_id=config_interpreter.talon_group_chat,
                                       text='testcase talon group')
            time.sleep(1)
            self.assertIsInstance(message, telebot.types.Message)
            bot.delete_message(chat_id=config_interpreter.talon_group_chat,
                               message_id=message.message_id)
        except Exception as e:
            print(type(e))
            self.fail("group not exist or test internet connection")

    def test_screenshot_group(self):
        bot = main.bot
        try:
            message = bot.send_message(chat_id=config_interpreter.screenshot_group_chat,
                                       text='testcase screenshot group')
            time.sleep(1)
            self.assertIsInstance(message, telebot.types.Message)
            bot.delete_message(chat_id=config_interpreter.screenshot_group_chat,
                               message_id=message.message_id)
        except Exception as e:
            print(type(e))
            self.fail("group not exist or test internet connection")


if __name__ == '__main__':
    unittest.main()

# todo create tests
# solved check internet connection
# solved  Server working
# solved  List existing
# solved  Talon loading
# solved  talon group check
# solved screenshot group check
# solved  pricelist correctly
# solved  loading info from server
# todo server test accept and decline sign
