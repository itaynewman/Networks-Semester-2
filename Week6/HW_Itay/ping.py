from scapy.all import *
import time


def ping(domain, count=3):
    ping_times = []

    for _ in range(count):
        packet = IP(dst=domain) / ICMP()
        start_time = time.time()
        reply = sr1(packet, timeout=1, verbose=0)
        end_time = time.time()

        if reply:
            elapsed_time = (end_time - start_time) * 1000  # Convert to milliseconds
            ping_times.append(elapsed_time)
            print(f"Reply from {reply.src}: time={elapsed_time:.2f}ms")
        else:
            print(f"Request to {domain} timed out.")

    if ping_times:
        average_time = sum(ping_times) / len(ping_times)
        print(f"Summary: Average={average_time:.2f}ms")
    else:
        print("No valid ping responses.")


if __name__ == "__main__":
    domain = input("Insert domain name: ")
    ping(domain)
