import socket
import datetime

SERVER_IP = "34.218.16.79"
SERVER_PORT = 77


def checksum_calc(location, date):
    location = location.lower()
    date = date.replace('/', '')
    checksum = 0

    letter_to_numbers = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5,
                         'f': 6, 'g': 7, 'h': 8, 'i': 9, 'j': 10,
                         'k': 11, 'l': 12, 'm': 13, 'n': 14, 'o': 15,
                         'p': 16, 'q': 17, 'r': 18, 's': 19, 't': 20,
                         'u': 21, 'v': 22, 'w': 23, 'x': 24, 'y': 25,
                         'z': 26}

    for char in location:
        if char in letter_to_numbers:
            checksum += letter_to_numbers[char]

    for digit in date:
        checksum += float(digit) * 0.01

    return "%.2f" % checksum


def parse_server_response(server_msg):
    parts = server_msg.split('&')
    data = {}
    for part in parts:
        key, value = part.split('=')
        data[key] = value
    return data


def check_forecast(city, date):
    temp = 0
    description = ""
    checksum = checksum_calc(city, date)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = (SERVER_IP, SERVER_PORT)
    sock.connect(server_address)

    server_msg = sock.recv(1024)
    server_msg = server_msg.decode()

    request_weather = f"100:REQUEST:city={city}&date={date}&checksum={checksum}"

    sock.sendall(request_weather.encode())

    server_msg = sock.recv(1024)
    server_msg = server_msg.decode()

    response_data = parse_server_response(server_msg)

    if 'temp' in response_data:
        temp = float(response_data['temp'])

    if 'text' in response_data:
        description = response_data['text']

    return temp, description


def display_weather(city, date):
    result = check_forecast(city, date)
    print(f"{date}, Temperature: {result[0]}, Description: {result[1]}.")


def sort_by_population(capital):
    return capital[2]


def print_capital_forecast():
    capitals_data = [
        ("China", "Beijing", 20693000),
        ("India", "New Delhi", 16787949),
        ("Japan", "Tokyo", 13189000),
        ("Philippines", "Manila", 12877253),
        ("Russia", "Moscow", 11541000),
        ("Egypt", "Cairo", 10230350),
        ("Indonesia", "Jakarta", 10187595),
        ("Democratic Republic of the Congo", "Kinshasa", 10125000),
        ("South Korea", "Seoul", 9989795),
        ("Mexico", "Mexico City", 8851080),
        ("Iran", "Tehran", 8846782),
        ("United Kingdom", "London", 8630100),
        ("Peru", "Lima", 8481415),
        ("Thailand", "Bangkok", 8249117),
        ("Germany", "Berlin", 3769495),
        ("Vietnam", "Hanoi", 7587800),
        ("Hong Kong", "Hong Kong", 7298600),
        ("Iraq", "Baghdad", 7216040),
        ("Singapore", "Singapore", 5535000),
        ("Turkey", "Ankara", 5150072)
    ]

    # Sort capitals data by population in descending order
    capitals_data.sort(key=sort_by_population, reverse=True)

    # Fetch and print forecast for each capital
    for i, (country, city, population) in enumerate(capitals_data, start=1):
        temp, description = check_forecast(city, datetime.datetime.now().strftime("%d/%m/%Y"))
        print(f"{i}. {city}, {temp} degrees.")


def main():
    city = input("Enter your city of residence: ")
    print("\nMenu:")
    print("1. Today's Weather")
    print("2. Next Three Days")

    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        today_date = datetime.datetime.now().strftime("%d/%m/%Y")
        display_weather(city, today_date)
    elif choice == '2':
        for i in range(3):
            future_date = (datetime.datetime.now() + datetime.timedelta(days=i+1)).strftime("%d/%m/%Y")
            display_weather(city, future_date)
    else:
        print("Invalid choice. Please enter 1 or 2.")

    print_capital_forecast()


if __name__ == "__main__":
    main()
