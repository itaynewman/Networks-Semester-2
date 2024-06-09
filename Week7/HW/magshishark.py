from scapy.all import TCP, sniff, IP, DNSRR
from scapy.layers.http import HTTPRequest, HTTPResponse
import re

WEATHER_SERVER_IP = "34.218.16.79"
WEATHER_SERVER_PORT = 77


def dns_filter(packet):
    return packet.haslayer(DNSRR)


def dns_process(packet):
    if dns_filter(packet):
        dns_layer = packet.getlayer(DNSRR)
        print(f"{dns_layer.rrname.decode()} ===> {dns_layer.rdata}")


def forecast_filter(packet):
    try:
        return packet.haslayer(IP) and packet[IP].src == WEATHER_SERVER_IP
    except AttributeError:
        pass
    except IndexError:
        pass
    return False


def forecast_process(packet):
    if forecast_filter(packet):
        try:
            payload = bytes(packet.payload).decode('utf-8', errors='ignore')
            match = re.search(r'(\d{3}:ANSWER:date=[\d/]+&city=[\w\s]+&temp=[\d.]+&text=[\w\s]+)', payload)
            if match:
                print(match.group(1))
        except UnicodeDecodeError:
            pass
        except IndexError:
            pass


def http_filter(packet):
    return packet.haslayer(HTTPRequest)


def http_process(packet):
    if http_filter(packet):
        http_layer = packet.getlayer(HTTPRequest)
        if http_layer.Method.decode() == 'GET':
            print(http_layer.Path.decode())


def email_filter(packet):
    return packet.haslayer(HTTPResponse)


def email_process(packet):
    if email_filter(packet):
        try:
            payload = bytes(packet[TCP].payload).decode('utf-8', errors='ignore')
            emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", payload)
            for email in emails:
                print(email)
        except UnicodeDecodeError:
            pass
        except IndexError:
            pass


options = {
    1: (dns_filter, dns_process),
    2: (forecast_filter, forecast_process),
    3: (http_filter, http_process),
    4: (email_filter, email_process),
}


def main():
    print("Welcome to Magshishark!")
    running = True
    while running:
        print("\nPlease select sniffing state:")
        print("1. DNS")
        print("2. Forecast")
        print("3. HTTP")
        print("4. E-mails")
        print("Or select 0 to Exit:")

        try:
            choice = int(input())
        except ValueError:
            print("Invalid input. Please enter a number between 0 and 4.")
            continue

        if choice == 0:
            print("Exiting program goodbye.")
            running = False
        elif choice in options:
            filter_func, process_func = options[choice]
            try:
                print("Sniffing... Press Ctrl+C to stop and return to menu.")
                sniff(prn=process_func, lfilter=filter_func)
            except KeyboardInterrupt:
                print("\nStopped sniffing. Returning to menu.")
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
