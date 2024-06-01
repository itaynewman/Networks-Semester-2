from scapy.all import *

# Constants
DNS_SERVER = "8.8.8.8"  # Google's DNS server
DNS_PORT = 53


def nslookup(domain):
    # Create IP layer
    ip_layer = IP(dst=DNS_SERVER)

    # Create UDP layer
    udp_layer = UDP(dport=DNS_PORT)

    # Create DNS layer with the query
    dns_layer = DNS(rd=1, qd=DNSQR(qname=domain))

    # Combine the layers to form the complete DNS request
    dns_request = ip_layer / udp_layer / dns_layer

    # Send the request and get the response
    response = sr1(dns_request, verbose=0)

    # Extract the IP address from the response
    if response and response.haslayer(DNS):
        for answer in response[DNS].an:
            if answer.type == 1:  # Check if the answer is of type A
                print(answer.rdata)


if __name__ == "__main__":
    domain = input("Insert domain name: ")
    nslookup(domain)
