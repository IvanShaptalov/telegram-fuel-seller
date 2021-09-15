import configparser
import os
from pathlib import Path

CORE_PATH = Path(__file__).resolve().parent
CONFIG_PATH = os.path.join(CORE_PATH, 'config.ini')
config = configparser.ConfigParser()

config.read(CONFIG_PATH)

BOT_TOKEN = config['Bot']['bot_token']
pre_alchemy_db_path = config['DataBase']['sql_alchemy_path']
server_token = config['Server']['token']
server_host = config['Server']['host']
source_type = 'telegram'
# card = config['Purchase']['card']
talon_group_chat = int(config['GroupChat']['talons'])
talon_group_link = config['GroupChat']['link_talons']
screenshot_group_chat = int(config['GroupChat']['screenshots'])
screenshot_group_link = config['GroupChat']['link_screen']
back_ref = config['Feedback']['feed']
alchemy_db_path = "sqlite:///" + os.path.join(CORE_PATH, pre_alchemy_db_path)

