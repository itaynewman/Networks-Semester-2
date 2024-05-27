import requests


def extract_password_from_site():
    url = "http://webisfun.cyber.org.il/nahman/files/"
    response = requests.get(url)
    password = ""
    if response.status_code == 200:
        files = response.text.splitlines()
        for i in range(11, 35):
            file_number = i
            file_url = f"{url}file{file_number}.nfo"  # Format the URL with file number
            file_response = requests.get(file_url)
            if file_response.status_code == 200:
                file_content = file_response.text
                password += file_content[99]
    return password


def main():
    print(extract_password_from_site())


if __name__ == '__main__':
    main()
