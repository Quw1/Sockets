from bottle import route, run, template, static_file, request
import socket
import logging
from methods import message_to_bytes, HEADER, PORT, FORMAT, CMDS, receive_server_message
from time import sleep
from random import randint, uniform


SERVER = 'xxx.xxx.xxx.xxx1'
ADDR = SERVER, PORT

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg: str):
    message, send_length = message_to_bytes(msg)

    client.send(send_length)

    resp = receive_server_message(client)
    if resp:
        if resp == CMDS['OVERFLOW']:
            logging.error('Overflow!')
        elif resp == CMDS['OK']:
            client.send(message)
    else:
        logging.error("Empty len")


@route('/')
def index():
    return static_file('index.html', '')


@route('/ajax', method='POST')
def ajax():
    c_num = request.forms.get('cNum')
    c_val = request.forms.get('cVal')
    to_do = request.forms.get('toDo')
    resp = ''

    if to_do == 'putOne':
        to_send = CMDS['PUT'] + f":{c_num}/{c_val}"
        send(to_send)
        resp = receive_server_message(client)

    if to_do == 'getAll':
        resp = {}
        for i in range(10):

            to_send = CMDS['GET'] + f":{i+1}"
            send(to_send)
            s_resp = receive_server_message(client)
            s_resp = s_resp.split(':')
            if s_resp[0] == CMDS['POST']:
                resp[f'{i+1}'] = s_resp[1]

    return {"response": resp}


run(host='localhost', port=8080)
