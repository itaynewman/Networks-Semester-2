from scapy.layers.inet import ICMP, IP
from scapy.sendrecv import sniff


def isEcho(packet):
    if ICMP in packet and packet[ICMP].type == 0:
        return True
    return False


def isIp(packet):
    if IP in packet:
        print("ping reply from", packet[IP].src)


def main():
    packets = sniff(count=4, lfilter=isEcho, prn=isIp)
    print(packets)


if __name__ == '__main__':
    main()
