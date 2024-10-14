import socket

def start_server(host='127.0.0.1', port=50000):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server dimulai di {host}:{port}, menunggu koneksi...")

    while True:
        conn, addr = server_socket.accept()
        print(f"Koneksi diterima dari {addr}")
        message = conn.recv(1024).decode()
        print(f"Pesan diterima: {message}")

        # Mengirim respons
        conn.send("Pesan diterima oleh server".encode())
        conn.close()

if __name__ == "__main__":
    start_server()
