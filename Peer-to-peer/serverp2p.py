import socket
import threading
import time

# Fungsi untuk menangani koneksi dari peer lain
def handle_peer_connection(peer_socket):
    while True:
        try:
            # Menerima data dari peer
            data = peer_socket.recv(1024)
            if not data:
                break
            # Mencetak pesan yang diterima
            print(f"Pesan diterima: {data.decode()}")
            # Mengirim kembali respons ke peer
            peer_socket.send("Pesan diterima oleh server".encode())
        except Exception as e:
            print(f"Kesalahan saat menerima data: {e}")
            break
    peer_socket.close()

# Fungsi untuk menjalankan server P2P
def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    server_socket.listen(5)
    print(f"Server dimulai di port {port}, menunggu koneksi...")

    while True:
        peer_socket, addr = server_socket.accept()
        print(f"Koneksi diterima dari {addr}")
        threading.Thread(target=handle_peer_connection, args=(peer_socket,)).start()

# Fungsi untuk mengirim pesan dan mengukur latency
def send_message(peer_address, message, num_messages):
    peer_host, peer_port = peer_address.split(':')
    peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        peer_socket.connect((peer_host, int(peer_port)))
    except Exception as e:
        print(f"Gagal terhubung ke {peer_address}: {e}")
        return

    latencies = []
    
    for i in range(num_messages):
        start_time = time.time()  # Catat waktu mulai
        peer_socket.send(message.encode())
        response = peer_socket.recv(1024).decode()
        end_time = time.time()  # Catat waktu akhir

        latency = end_time - start_time
        latencies.append(latency)
        print(f"Pesan {i + 1}: Respons dari server: {response} | Latency: {latency:.4f} detik")

    # Menghitung rata-rata dan maksimum latensi
    average_latency = sum(latencies) / num_messages
    max_latency = max(latencies)

    # Menampilkan ringkasan hasil pengujian
    print("\n--- Test Summary ---")
    print(f"Jumlah pesan yang dikirim: {num_messages}")
    print(f"Average Latency: {average_latency:.4f} detik")
    print(f"Max Latency: {max_latency:.4f} detik")

    peer_socket.close()

if __name__ == "__main__":
    mode = input("Apakah Anda ingin menjalankan server (s) atau mengirim pesan (c)? ")

    if mode.lower() == 's':
        port = int(input("Masukkan port untuk server: "))
        start_server(port)
    elif mode.lower() == 'c':
        peer_address = input("Masukkan alamat peer (format: 127.0.0.1:50000): ")
        message = input("Masukkan pesan yang ingin dikirim: ")
        num_messages = int(input("Masukkan jumlah pesan yang ingin dikirim: "))
        send_message(peer_address, message, num_messages)
    else:
        print("Pilihan tidak valid.")
