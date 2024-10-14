import socket
import time

def send_message(peer_address, message, num_messages):
    peer_host, peer_port = peer_address.split(':')
    peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        peer_socket.connect((peer_host, int(peer_port)))
    except ConnectionRefusedError:
        print(f"Tidak dapat terhubung ke server di {peer_address}. Pastikan server berjalan.")
        return

    latencies = []
    for _ in range(num_messages):
        start_time = time.time()  # Waktu mulai pengiriman
        peer_socket.send(message.encode())
        response = peer_socket.recv(1024).decode()  # Menerima respons
        end_time = time.time()  # Waktu selesai pengiriman

        latency = end_time - start_time  # Menghitung latensi
        latencies.append(latency)

        print(f"Pesan '{message}' dikirim. Respons dari server: '{response}'. Latensi: {latency:.4f} detik")

    peer_socket.close()

    # Ringkasan pengujian
    if latencies:
        avg_latency = sum(latencies) / len(latencies)
        print(f"\n=== Test Summary ===")
        print(f"Jumlah pesan dikirim: {num_messages}")
        print(f"Latensi rata-rata: {avg_latency:.4f} detik")
        print(f"Pengiriman pesan selesai.\n")

if __name__ == "__main__":
    peer_address = input("Masukkan alamat peer (format: 127.0.0.1:50000): ")
    message = input("Masukkan pesan yang ingin dikirim: ")
    num_messages = int(input("Masukkan jumlah pesan yang ingin dikirim: "))
    
    # Memastikan jumlah pesan yang valid
    if num_messages <= 0:
        print("Jumlah pesan harus lebih besar dari 0.")
    else:
        send_message(peer_address, message, num_messages)
