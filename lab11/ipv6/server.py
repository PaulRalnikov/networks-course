import socket

def start_server(host='::1', port=12345):
    server_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

    server_socket.bind((host, port))

    server_socket.listen(5)
    print(f"Server launched on {host}:{port}. Waiting for connection...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connected to {addr}")

        data = client_socket.recv(1024)
        if not data:
            client_socket.close()
            print("No data")
            break
        data = data.decode()

        response = data.upper()
        client_socket.sendall(response.encode())

        client_socket.close()
        if (data == "exit"):
            client_socket.close()
            print("Finished")
            break

if __name__ == "__main__":
    start_server()
