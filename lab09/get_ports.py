import socket
import sys

def check_port(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        result = sock.connect_ex((ip, port))
        return result != 0

def find_free_ports(ip, start_port, end_port):
    free_ports = []
    for port in range(start_port, end_port + 1):
        if check_port(ip, port):
            free_ports.append(port)
    return free_ports

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python find_free_ports.py <IP-адрес> <start_port> <end_port>")
        sys.exit(1)

    ip_address = sys.argv[1]
    start_port = int(sys.argv[2])
    end_port = int(sys.argv[3])

    if start_port < 1 or end_port > 65535 or start_port > end_port:
        print("Ports have to be integers from 1 to 65535 and start port have not to be biggen than end port")
        sys.exit(1)

    free_ports = find_free_ports(ip_address, start_port, end_port)

    print(f"free ports on {ip_address} in range {start_port}-{end_port}:")
    for port in free_ports:
        print(port)
