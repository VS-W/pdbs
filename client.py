from socket import socket
from sys import argv

if len(argv) > 0:
    host = '127.0.0.1'
    port = 5999
    client_socket = socket()
    client_socket.connect((host, port))
    print(f'Connecting to {host}:{port}...')

    message = " ".join(argv[1:]).strip().encode()
    if len(message) > 0:
        print(f'Sending: {message.decode()}')
        client_socket.send(message)

    client_socket.close()
