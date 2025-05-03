import socket
import os
import struct
import time
import argparse

ICMP_ECHO_REQUEST = 8

def checksum(source_string):
    sum = 0
    for i in range(0, len(source_string), 2):
        if i + 1 < len(source_string):
            w = (source_string[i] << 8) + source_string[i + 1]
        else:
            w = source_string[i]
        sum = (sum + w) & 0xFFFF
    return ~sum & 0xFFFF

def create_packet(id):
    header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, 0, id, 1)
    data = bytes(56)
    my_checksum = checksum(header + data)
    header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), id, 1)
    return header + data

def send_packet(host, ttl, timeout):
    """
    Send ICMP request to host
    Returns tuple (hostname, ICMP request type, RTT in ms)
    """
    icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))
    icmp_socket.settimeout(timeout)
    icmp_socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)

    packet_id = os.getpid() & 0xFFFF
    packet = create_packet(packet_id)

    icmp_socket.sendto(packet, (host, 1))

    start_time = time.time()
    result = None
    try:
        recv_packet, addr = icmp_socket.recvfrom(1024)
        rtt_ms = int((time.time() - start_time) * 1000)
        addr = addr[0]
        try:
            hostname = socket.gethostbyaddr(addr)[0]
        except:
            hostname = addr

        icmp_header = recv_packet[20:21]
        icmp_type = struct.unpack('b', icmp_header)[0]

        result = (hostname, icmp_type, rtt_ms)
    except socket.timeout:
        pass
    finally:
        icmp_socket.close()
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("host", type = str, help="Target host")
    parser.add_argument("--count", type = int, default = 3, help="Count packet per host")
    parser.add_argument("--timeout", type = int, default = 2, help="Timeout for each packet (seconds)")

    args = parser.parse_args()

    target_host = args.host
    count = args.count
    timeout = args.timeout

    ttl = 1
    while True:
        result = None
        for _ in range(count):
            result = send_packet(target_host, ttl, timeout)
            if result is not None:
                break

        if result is None:
            print(f"Can not find server with ttl = {ttl}; skipped")
            ttl += 1
            continue

        host, icmp_type, rtt_ms = result
        print(f"Request from {host}; ttl = {ttl}, type = {icmp_type}, rtt = {rtt_ms}ms")

        if (icmp_type == 0):
            break
        else:
            ttl += 1

