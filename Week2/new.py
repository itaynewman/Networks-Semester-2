import socket
SERVER_IP = "networks.cyber.org.il"
SERVER_PORT = 8820

def connect_to_server():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = (SERVER_IP, SERVER_PORT)
    sock.connect(server_address)

    msg = "hello2"
    sock.sendall(msg.encode())

    server_msg = sock.recv(1024)
    server_msg = server_msg.decode()

    print(server_msg)

connect_to_server()
