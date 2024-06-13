from scapy.all import *
from scapy.layers.inet import IP, UDP
import hashlib

ALIEN_IP = '54.71.128.194'
last_ten_chars_list = []


def filter_func(packet):
    """
    Filter function to check if a packet is from or to the ALIEN_IP.

    Args:
        packet (scapy.packet.Packet): The packet to be checked.

    Returns:
        bool: True if the packet is from or to the ALIEN_IP, False otherwise.
    """
    return IP in packet and (packet[IP].src == ALIEN_IP or packet[IP].dst == ALIEN_IP)


def custom_cipher_decipher(string, caesar_key):
    """
    Custom cipher to decipher a string using a Caesar cipher.

    Args:
        string (str): The string to be deciphered.
        caesar_key (str): The Caesar cipher key containing the error number.

    Returns:
        str: The deciphered string.
    """
    error_number = int(caesar_key[-3:])
    result = []

    for i, char in enumerate(string):
        if i % 2 != 0 or not char.isalpha():
            result.append(char)
        else:
            base = ord('a') if char.islower() else ord('A')
            new_char = chr((ord(char) - base - error_number) % 26 + base)
            result.append(new_char)

    return ''.join(result)


def extract_caesar_key(payload):
    """
    Extract the Caesar cipher key from the payload.

    Args:
        payload (str): The payload containing the Caesar cipher key.

    Returns:
        str: The Caesar cipher key, or None if not found.
    """
    for i in range(len(payload) - 6):
        if payload[i + 3:i + 6].isdigit():
            return payload[i:i + 6]
    return None


def handle_packet(packet):
    """
    Handle incoming packets, decipher payloads, and send new packets with MD5 hash.

    Args:
        packet (scapy.packet.Packet): The incoming packet to be handled.
    """
    if not filter_func(packet) or Raw not in packet:
        return

    payload = packet[Raw].load.decode()
    caesar_key = extract_caesar_key(payload)

    if not caesar_key:
        return

    deciphered_payload = custom_cipher_decipher(payload[len(caesar_key):], caesar_key)
    print(deciphered_payload)

    if "location data" in deciphered_payload:
        last_ten_chars = deciphered_payload[-10:]
        last_ten_chars_list.append(last_ten_chars)

    if "location data 10/10:" in deciphered_payload:
        all_last_ten_chars = ''.join(last_ten_chars_list)[:100]
        md5_hash = hashlib.md5(all_last_ten_chars.encode()).hexdigest()
        new_payload = (
            f"FLY000location_md5={md5_hash},airport=nevada25.84,time=15:52,"
            f"lane=earth.jup,vehicle=2554,fly"
        )
        new_packet = IP(dst=ALIEN_IP) / UDP(sport=packet[IP].dport, dport=packet[IP].sport) / Raw(load=new_payload)
        send(new_packet)
        print("Sent packet:", new_payload)


def main():
    """
    Main function to start sniffing packets and handle them.
    """
    sniff(prn=handle_packet)


if __name__ == '__main__':
    main()
