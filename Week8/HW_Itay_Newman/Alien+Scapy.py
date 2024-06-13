from scapy.all import *
from scapy.layers.inet import IP, UDP
import hashlib

ALIEN_IP = '54.71.128.194'


def filter_func(packet):
    return IP in packet and (packet[IP].src == ALIEN_IP or packet[IP].dst == ALIEN_IP)


def custom_cipher_decipher(string, caesar_key):
    error_number = int(caesar_key[-3:])
    result = []
    for i, char in enumerate(string):
        if i % 2 != 0 or not char.isalpha():
            result.append(char)
        else:
            new_char = chr((ord(char) - ord('a') - error_number) % 26 + ord('a')) if char.islower() else chr((ord(char) - ord('A') - error_number) % 26 + ord('A'))
            result.append(new_char)
    return ''.join(result)


def extract_caesar_key(payload):
    for i in range(len(payload) - 6):
        if payload[i + 3:i + 6].isdigit():
            return payload[i:i + 6]
    return None


def handle_packet(packet):
    global last_ten_chars_list
    if filter_func(packet):
        payload = packet[Raw].load.decode()
        caesar_key = extract_caesar_key(payload)
        if caesar_key:
            deciphered_payload = custom_cipher_decipher(payload[len(caesar_key):], caesar_key)
            print("Deciphered payload:", deciphered_payload)
            if "location data" in deciphered_payload:
                last_ten_chars = deciphered_payload[-10:]
                last_ten_chars_list.append(last_ten_chars)

            if "location data: 10/10" in deciphered_payload:
                all_last_ten_chars = ''.join(last_ten_chars_list)
                all_last_ten_chars = all_last_ten_chars[:100]
                md5_hash = hashlib.md5(all_last_ten_chars.encode()).hexdigest()
                new_payload = f"FLY000location_md5={md5_hash},airport=nevada25.84,time=15:52,lane=earth.jup,vehicle=2554,fly"
                new_packet = IP(dst=ALIEN_IP) / UDP(dport=packet[IP].sport) / Raw(load=new_payload)
                send(new_packet)
                print("Sent packet:", new_payload)
        else:
            print("Caesar key not found in the payload.")


def main():
    global last_ten_chars_list
    last_ten_chars_list = []
    sniff(prn=handle_packet)


if __name__ == '__main__':
    main()
