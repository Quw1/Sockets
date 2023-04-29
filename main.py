import socket
import threading
import logging
from time import sleep
from random import randint, uniform
from methods import HEADER, PORT, FORMAT, CMDS, send_message_to_client


logging.basicConfig(handlers=[
                        logging.FileHandler("file.log"),
                        logging.StreamHandler()
                    ],
                    level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')


MESSAGE_MAX_LEN = 255*8
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

VARS = [
    '',
    [1, 1],
    [2, 1],
    [3, 1],
    [4, 1],
    [5, 1],
    [6, 1],
    [7, 1],
    [8, 1],
    [9, 1],
    [10, 1]
]


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    logging.warning(f'[CONNECT] {addr[0]} ({addr[1]}) connected.')

    try:

        connected = True
        while connected:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)

                if msg_length > MESSAGE_MAX_LEN:
                    send_message_to_client(CMDS['OVERFLOW'], conn)
                else:
                    send_message_to_client(CMDS['OK'], conn)

                    msg_list = conn.recv(msg_length).decode(FORMAT).split('&')
                    msg_list = [i for i in msg_list if i != '']
                    for msg in msg_list:
                        logging.info(f'[SOCKET] From {addr[0]} ({addr[1]}) : "{msg}"')

                        cmd_args = msg.split(':')
                        cmd_check = cmd_args[0]

                        to_send = ''

                        if cmd_check == CMDS['DISCONNECT']:
                            logging.warning(f'[DISCONNECT] {addr[0]} ({addr[1]}) disconnected.')
                            connected = False
                            break
                        elif cmd_check == CMDS['PUT']:
                            try:
                                cmd_args = cmd_args[1].split('/')
                                cnum = int(cmd_args[0])
                                cval = int(cmd_args[1])

                                if VARS[cnum][1]:
                                    VARS[cnum][0] = cval

                                    logging.info(f'[VARS_CHANGE] - Access Granted for {addr[0]} ({addr[1]}) | Var#{cnum} -> {cval}')
                                    to_send = CMDS['OK']
                                else:
                                    logging.info(f'[VARS_CHANGE] - Access Denied for {addr[0]} ({addr[1]}) | Tried changing Var#{cnum} -> {cval}')
                                    to_send = CMDS['DENIED']

                            except Exception as e:
                                to_send = CMDS['ERROR'] + ':' + str(e)
                                logging.error(f'[ERROR] PUT - {e}')

                        elif cmd_check == CMDS['GET']:
                            try:
                                cnum = int(cmd_args[1])
                                cval = str(VARS[cnum][0])
                                to_send = CMDS['POST'] + ':' + cval
                                logging.info(f'[VARS_STATE] - {addr[0]} ({addr[1]}) Read #{cnum} = {cval}')

                            except Exception as e:
                                to_send = CMDS['ERROR'] + ':' + str(e)
                                logging.error(f'[ERROR] GET - {e}')

                        elif cmd_check == CMDS['WHOAMI']:
                            to_send = 'Tkachenko Timur :: V-24 / Mutual Variables Dispatcher'

                        else:
                            logging.info(f'[INVALID] Invalid command by {addr[0]} ({addr[1]})')
                            to_send = CMDS['INVALID']

                        send_message_to_client(to_send, conn)

    except ConnectionResetError:
        logging.error(f'[ERROR] Client ({addr[0]} {addr[1]}) forcibly closed connection.')

    conn.close()


def vars_dispatcher():
    while True:
        if randint(0, 1):
            to_change = randint(1, 10)
            VARS[to_change][1] = 1 - VARS[to_change][1]
            # print(f'changing {to_change} to {VARS[to_change][1]}')
            sleep(round(uniform(0.02, 0.1), 3))


def start():
    logging.warning('[SERVER] Server is starting...')
    server.listen()
    logging.warning(f'[SERVER] Server started. Running @ {SERVER}')

    disp = threading.Thread(target=vars_dispatcher, daemon=True)
    disp.start()

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        thread.start()
        logging.warning(f'[SERVER] Active connections: [{threading.active_count() - 1}]')


if __name__ == "__main__":
    start()


