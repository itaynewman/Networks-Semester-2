import socket

LISTEN_HOST = '127.0.0.1'
LISTEN_PORT = 9090
SERVER_HOST = '54.71.128.194'
SERVER_PORT = 92


def listen():
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.bind((LISTEN_HOST, LISTEN_PORT))
    listen_socket.listen(5)
    print(f'Listening on {LISTEN_HOST}:{LISTEN_PORT}')
    return listen_socket


def connect_to_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((SERVER_HOST, SERVER_PORT))
    return server_socket


def handle_request(client_socket, server_socket):
    request = client_socket.recv(4096)
    print('Received request from client:')
    print(request.decode())

    server_socket.sendall(request)
    print('Sent request to server:', request.decode())

    response = server_socket.recv(4096)
    print('Received response from server:')
    print(response.decode())
    return response


def modify_response(response, request):
    modified_response = ''
    response = response.decode()
    if "name:" in response:
        modified_response = response.replace('name:"', 'name:"Proxy: ')
        index = modified_response.find("jpg")
        modified_response = modified_response[:index] + '.' + modified_response[index:]
        if "France" in request.decode():
            modified_response = 'ERROR#"France is banned!"'
    else:
        if 'End year is less or equal to start year"' in response:
            modified_response = 'ERROR#"Negative difference between the years"'
        else:
            modified_response = 'ERROR#"Unknown Genre"'
    return modified_response.encode()


def close_sockets(client_socket, server_socket, listen_socket):
    client_socket.close()
    server_socket.close()
    listen_socket.close()


def proxy():
    listen_socket = listen()
    server_socket = connect_to_server()

    while True:
        client_socket, client_address = listen_socket.accept()
        print(f'Accepted connection from {client_address[0]}:{client_address[1]}')

        response = handle_request(client_socket, server_socket)

        modified_response = modify_response(response, client_socket)

        client_socket.sendall(modified_response)
        print('Sent modified response to client:', modified_response)

        close_sockets(client_socket, server_socket, listen_socket)


def main():
    proxy()


if __name__ == '__main__':
    main()
