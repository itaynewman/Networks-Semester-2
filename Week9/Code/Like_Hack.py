import socket

SERVER_IP = "54.187.16.171"
SERVER_PORT = 1336
MESSAGE = """710#{gli&&er}{"glit_id":45213,"user_id":42778,"user_screen_name":"zxcvbnm","id":-1}"""


def main():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    try:
        server_address = (SERVER_IP, SERVER_PORT)
        print(f"Connecting to {SERVER_IP} port {SERVER_PORT}")
        sock.connect(server_address)
    except Exception as e:
        print(f"Failed to connect: {e}")
        return

    # Send the message 10 times
    try:
        for i in range(10):
            print(f"Sending message {i + 1}")
            sock.sendall(MESSAGE.encode('utf-8'))
    except Exception as e:
        print(f"An error occurred while sending data: {e}")

    # Close the socket
    print("Closing connection")
    sock.close()


if __name__ == "__main__":
    main()
