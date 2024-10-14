import socket
import time
import threading
from datetime import datetime

def client_test(host='127.0.0.1', port=50000, message='Hallo'):
    """Fungsi klien untuk mengirim pesan dan menerima respons dari server."""
    start_time = datetime.now()
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((host, port))
            client_socket.send(message.encode())
            response = client_socket.recv(1024).decode()
            end_time = datetime.now()
            latency = (end_time - start_time).total_seconds()
            print(f"Client: {message} | Respons: {response} | Latensi: {latency:.4f} detik")
            return latency
    except Exception as e:
        print(f"Kesalahan: {e}")
        return None

def run_tests(num_clients=5):
    """Fungsi untuk menjalankan pengujian dengan jumlah klien tertentu."""
    latencies = []
    threads = []

    for _ in range(num_clients):
        thread = threading.Thread(target=lambda: latencies.append(client_test()))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return latencies

def summarize_results(latencies):
    """Fungsi untuk merangkum hasil pengujian."""
    if latencies:
        avg_latency = sum(latencies) / len(latencies)
        print(f"\nRingkasan Hasil Pengujian:")
        print(f"Total Klien: {len(latencies)}")
        print(f"Rata-rata Latensi: {avg_latency:.4f} detik")
        print(f"Throughput: {len(latencies) / sum(latencies):.2f} klien per detik")
    else:
        print("Tidak ada latensi yang tercatat.")

if __name__ == "__main__":
    for client_count in [5, 10, 20]:
        print(f"\nMenjalankan pengujian dengan {client_count} klien...")
        latencies = run_tests(num_clients=client_count)
        summarize_results(latencies)
