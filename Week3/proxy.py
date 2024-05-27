import socket


def proxy():
    listen_host = '127.0.0.1'
    listen_port = 9090

    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.bind((listen_host, listen_port))
    listen_socket.listen(5)
    print(f'Listening on {listen_host}:{listen_port}')

    with open('C:\\Users\\Cyber_User\\Documents\\Magshimim\\Networks Semester 2\\Week3\\blacklist.txt') as f:
        txt = f.read()

    while True:
        client_socket, client_address = listen_socket.accept()
        print(f'Accepted connection from {client_address[0]}:{client_address[1]}')

        request = client_socket.recv(4096)
        print('Received request from client:')
        print(request.decode())

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_host = '54.71.128.194'
        server_port = 92
        server_socket.connect((server_host, server_port))

        server_socket.sendall(request)
        print('Sent request to server:', request.decode())

        response = server_socket.recv(4096)
        print('Received response from server:')
        print(response.decode())
        response = response.decode()

        modified_response = ''
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

        modified_response = modified_response.encode()
        client_socket.sendall(modified_response)
        print('Sent modified response to client:', modified_response)

        server_socket.close()
        client_socket.close()


def main():
    proxy()


if __name__ == '__main__':
    main()
