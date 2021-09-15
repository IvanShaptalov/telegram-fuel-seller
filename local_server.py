import json
from icecream import ic
from bottle import run, post, request, route

import main
from statements.purchase_menu.callback_handler.talon_operations import send_tokens


# todo add token to path
@post('/add')
def process():
    post_data = request.body.read()
    data = json.loads(post_data)
    # kill - fuser -n tcp -k 3472
    if send_tokens(data):
        return "tokens_send"
    else:
        return "bad request or token list is empty"


@post('/decline')
def decline():
    post_data = request.body.read()
    data = json.loads(post_data)
    try:
        bot = main.bot
        bot.send_message(chat_id=data['chat_id'],
                         text=data['text'])
    except Exception as e:
        print(e, type(e))
        return 'bad request'
    else:
        return '200'


@route('/index')
def index():
    return '200'


PORT = 3472


def run_listener():
    ic('listener run')
    run(host='localhost', port=PORT, debug=True)


if __name__ == '__main__':
    run_listener()
