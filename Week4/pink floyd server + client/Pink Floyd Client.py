import socket

SERVER_IP = '127.0.0.1'
SERVER_PORT = 170


def get_user_input():
    """
    Get user input
    :return decision to main:
    """
    choice = input("Enter command: ")

    if choice == '1':
        return "1"
    elif choice == '2':
        album_name = input("Enter album name: ")
        return f"2&{album_name}"
    elif choice == '3':
        song_name = input("Enter song name: ")
        return f"3&{song_name}"
    elif choice == '4':
        song_name = input("Enter song name: ")
        return f"4&{song_name}"
    elif choice == '5':
        song_name = input("Enter song name: ")
        return f"5&{song_name}"
    elif choice == '6':
        search_text = input("Enter search text: ")
        return f"6&{search_text}"
    elif choice == '7':
        search_text = input("Enter search text: ")
        return f"7&{search_text}"
    elif choice == '8':
        return "8"
    elif choice == '9':
        return "9"
    elif choice == '10':
        return "10"
    else:
        print("Invalid command")
        return None


def main():
    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((SERVER_IP, SERVER_PORT))

            welcome_message = client.recv(1024).decode()
            print(f"Client received: {welcome_message}")

            while True:
                menu = client.recv(1024).decode()
                print(menu)

                user_input = get_user_input()

                if user_input:
                    client.send(user_input.encode())

                    response = client.recv(1024).decode()
                    print(f"Server response: {response}")

                    if user_input.startswith('10'):
                        break

            client.close()
            break

        except (ConnectionResetError, BrokenPipeError):
            print("Connection lost. Attempting to reconnect...")
            client.close()

        except Exception as e:
            print(f"An error occurred: {e}")
            client.close()
            break


if __name__ == "__main__":
    main()
