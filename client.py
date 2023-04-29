# import socket
# import logging
# from methods import message_to_bytes, HEADER, PORT, FORMAT, CMDS, receive_server_message
# from time import sleep
# from random import randint, uniform
#
#
# logging.basicConfig(handlers=[
#                         logging.StreamHandler()
#                     ],
#                     level=logging.DEBUG,
#                     format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
#
#
# SERVER = '192.168.223.1'
# ADDR = SERVER, PORT
#
#
# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect(ADDR)
#
#
# def send(msg: str):
#     message, send_length = message_to_bytes(msg)
#
#     client.send(send_length)
#
#     resp = receive_server_message(client)
#     if resp:
#         if resp == CMDS['OVERFLOW']:
#             logging.error('Overflow!')
#         elif resp == CMDS['OK']:
#             client.send(message)
#     else:
#         logging.error("Empty len")
#
#
# for i in range(5):
#     cNum = 2
#     cVal = 1
#     toSend = "?PUT:2/5"
#     send(toSend)
#     resp = receive_server_message(client)
#     print(resp)
#     sleep(round(uniform(0.1, 0.3), 3))
# send(CMDS['DISCONNECT'])
#
