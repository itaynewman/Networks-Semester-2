import socket
import data

# Constants
SERVER_IP = '127.0.0.1'
SERVER_PORT = 170
BUFFER_SIZE = 1024
MENU = """
Commands:
1. Request Albums
2. Request Songs in Album
3. Request Song Length
4. Request Song Lyrics
5. Request Album for Song
6. Search Song by Name
7. Search Song by Lyrics
8. Get Most Common Words
9. Get Albums Sorted by Length
10. Exit
"""
WELCOME_MESSAGE = "Welcome to the Pink Floyd server!"
EXIT_COMMAND = "10"
FILE_PATH = "Pink_Floyd_DB.txt"  # Use a relative path

# Parse the data file
albums, songs = data.parse_data(FILE_PATH)


def get_albums():
    return data.get_albums(albums, songs)


def get_songs_in_album(album_name):
    return data.get_songs_in_album(albums, songs, album_name)


def get_song_length(song_name):
    return data.get_song_length(albums, songs, song_name)


def get_song_lyrics(song_name):
    return data.get_song_lyrics(albums, songs, song_name)


def get_album_for_song(song_name):
    return data.get_album_for_song(albums, songs, song_name)


def search_song_by_name(search_text):
    return data.search_song_by_name(albums, songs, search_text)


def search_song_by_lyrics(search_text):
    return data.search_song_by_lyrics(albums, songs, search_text)


def get_most_common_words():
    return data.get_most_common_words(albums, songs)


def get_albums_sorted_by_length():
    return data.get_albums_sorted_by_length(albums, songs)


def handle_request(request):
    command, *args = request.split('&')
    if command == '1':
        return get_albums()
    elif command == '2':
        return get_songs_in_album(*args)
    elif command == '3':
        return get_song_length(*args)
    elif command == '4':
        return get_song_lyrics(*args)
    elif command == '5':
        return get_album_for_song(*args)
    elif command == '6':
        return search_song_by_name(*args)
    elif command == '7':
        return search_song_by_lyrics(*args)
    elif command == '8':
        return get_most_common_words()
    elif command == '9':
        return get_albums_sorted_by_length()
    elif command == EXIT_COMMAND:
        return "Thank you for using the Pink Floyd Server! Bye Bye!"
    else:
        return "The requested item was not found."


def handle_client(client_socket):
    try:
        client_socket.send(WELCOME_MESSAGE.encode())
        while True:
            client_socket.send(MENU.encode())  # Send the menu to the client
            request = client_socket.recv(BUFFER_SIZE).decode()
            print(request)
            if not request:
                break

            response = handle_request(request)
            client_socket.send(response.encode())

            if request.startswith(EXIT_COMMAND):
                break
    except (socket.error, ConnectionResetError) as e:
        print(f"Connection error: {e}")
    finally:
        client_socket.close()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_IP, SERVER_PORT))
    server.listen(5)
    print(f"Server listening on {SERVER_IP}:{SERVER_PORT}")

    while True:
        try:
            client_socket, addr = server.accept()
            print(f"Accepted connection from {addr}")
            handle_client(client_socket)
        except Exception as e:
            print(f"Error accepting connection: {e}")


if __name__ == "__main__":
    main()
