HEADER = 8
PORT = 1049
FORMAT = 'utf-8'
CMDS = {
    'DISCONNECT': '?DSC',
    'OVERFLOW': '!OVF',
    'OK': '!OK',
    'PUT': '?PUT',
    'ERROR': '!ERR',
    'WHOAMI': 'Who',
    'INVALID': '!INV',
    'DENIED': '!DEN',
    'GET': '?GET',
    'POST': '?POST'
}


def message_to_bytes(msg):
    msg += '&'
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))

    return message, send_length


def send_message_to_client(msg, instance):
    message, send_length = message_to_bytes(msg)
    instance.send(send_length)
    instance.send(message)


def receive_server_message(instance):
    receive_length = instance.recv(HEADER).decode(FORMAT)
    if receive_length:
        receive_length = int(receive_length)
        response = instance.recv(receive_length).decode(FORMAT).split('&')[0]
        return response
    else:
        return None
