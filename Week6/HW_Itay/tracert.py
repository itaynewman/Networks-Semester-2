from scapy.all import *
import time


def tracert(domain, max_hops=30, timeout=2):
    ttl = 1
    while ttl <= max_hops:
        packet = IP(dst=domain, ttl=ttl) / ICMP()
        start_time = time.time()
        reply = sr1(packet, timeout=timeout, verbose=0)
        end_time = time.time()

        if reply is None:
            print(f"{ttl}: Request timed out.")
        elif reply.type == 11:
            elapsed_time = (end_time - start_time) * 1000  # Convert to milliseconds
            print(f"{ttl}: {reply.src} (time={elapsed_time:.2f}ms)")
        elif reply.type == 0:
            elapsed_time = (end_time - start_time) * 1000  # Convert to milliseconds
            print(f"{ttl}: {reply.src} (time={elapsed_time:.2f}ms)")
            print("Trace complete.")
            break
        else:
            print(f"{ttl}: Unexpected reply type {reply.type} from {reply.src}")

        ttl += 1


if __name__ == "__main__":
    domain = input("Insert domain name: ")
    tracert(domain)
