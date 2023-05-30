from socket import socket
from sys import argv

if len(argv) > 0:
    host = 'localhost'
    port = 5999
    client_socket = socket()
    client_socket.connect((host, port))
    print(f'Connecting to {host}:{port}...')

    for i, arg in enumerate(argv[1:]):
        print(f'Argument {i}: {arg}')
        message = arg.strip().encode()
        if len(message) > 0:
            client_socket.send(message)
            data = client_socket.recv(1024).decode()
            print(f'Server: {data}')

    client_socket.close()
