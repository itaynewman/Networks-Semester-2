from scapy.all import *
from scapy.layers.inet import IP

ALIEN_IP = '54.71.128.194'


def filter_func(packet):
    return IP in packet and packet[IP].src == ALIEN_IP


def custom_cipher_decipher(string, caesar_key):
    error_number = int(caesar_key[-3:])
    result = []
    for i, char in enumerate(string):
        if i % 2 != 0 or not char.isalpha():
            result.append(char)
        else:
            new_char = chr((ord(char) - ord('a') - error_number) % 26 + ord('a')) if char.islower() else chr(
                (ord(char) - ord('A') - error_number) % 26 + ord('A'))
            result.append(new_char)
    return ''.join(result)


def extract_caesar_key(payload):
    for i in range(len(payload) - 6):
        if payload[i + 3:i + 6].isdigit():
            return payload[i:i + 6]
    return None


def handle_packet(packet):
    if filter_func(packet):
        payload = packet[Raw].load.decode()
        caesar_key = extract_caesar_key(payload)
        if caesar_key:
            deciphered_payload = custom_cipher_decipher(payload[len(caesar_key):], caesar_key)
            print("Deciphered payload:", deciphered_payload)
        else:
            print("Caesar key not found in the payload.")


def main():
    sniff(prn=handle_packet)


if __name__ == '__main__':
    main()
