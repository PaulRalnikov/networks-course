import socket

def start_client(host='::1', port=12345):
    while True:
        message = input("Enter message: ")
        if (len(message) == 0):
            print("Can not send empty message")
            break

        client_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

        client_socket.connect((host, port))
        client_socket.sendall(message.encode())

        response = client_socket.recv(1024)
        print(f"Server responce: {response.decode()}")

        client_socket.close()

if __name__ == "__main__":
    start_client()
