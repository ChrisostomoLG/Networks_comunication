import socket
import time


def tcp_server(host='localhost', port=5001):
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_socket.bind((host, port))
    servidor_socket.listen(1)

    print(f"Servidor TCP aguardando conexões em {host}:{port}")
    conn, addr = servidor_socket.accept()

    start_time = time.time()  # Inicia contagem de tempo

    with conn:
        print(f"Conexão estabelecida com {addr}")

        # Recebe o tamanho do arquivo
        file_size_bytes = conn.recv(8)
        file_size = int.from_bytes(file_size_bytes, byteorder='big')

        received_bytes = 0
        received_data = b""

        # Recebe os dados do arquivo
        while received_bytes < file_size:
            data = conn.recv(1024)
            received_data += data
            received_bytes += len(data)

        # Salva o arquivo recebido
        nome_arquivo_recebido = 'arquivorecebido.txt'
        with open(nome_arquivo_recebido, 'wb') as f:
            f.write(received_data)

        print(f"Arquivo recebido e salvo como {nome_arquivo_recebido}. Tamanho: {received_bytes} bytes")

    end_time = time.time()  # Finaliza contagem de tempo
    print(f"Tempo total de recepção (TCP): {end_time - start_time:.6f} segundos")


if __name__ == "__main__":
    tcp_server()