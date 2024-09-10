import socket
import time
import zlib


def servidor_udp(host='localhost', port=5002):
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servidor_socket.bind((host, port))

    print(f"Servidor UDP aguardando conexões em {host}:{port}")

    bytes_recebidos = 0
    dados_recebidos = b""
    tamanho_esperado = None
    endereco = None

    # Recebe o tamanho do arquivo
    while True:
        dado, endereco = servidor_socket.recvfrom(1024)
        if len(dado) == 8:
            tamanho_esperado = int.from_bytes(dado, byteorder='big')
            break

    # Recebe os dados do arquivo
    while bytes_recebidos < tamanho_esperado:
        tempo_inicio = time.time()  # Inicia contagem de tempo
        dado, _ = servidor_socket.recvfrom(1028)  # 4 bytes para o checksum + 1024 bytes de dados
        if len(dado) < 4:
            print("Erro: Pacote inválido recebido.")
            continue

        checksum = int.from_bytes(dado[:4], byteorder='big')
        chunk = dado[4:]

        if zlib.crc32(chunk) != checksum:
            print("Erro: Checksum inválido. Pacote descartado.")
            continue

        dados_recebidos += chunk
        bytes_recebidos += len(chunk)

    # Salva o arquivo recebido
    filename = 'arquivorecebido.txt'
    with open(filename, 'wb') as f:
        f.write(dados_recebidos)

    print(f"Arquivo recebido e salvo como {filename}")

    tempo_fim = time.time()  # Finaliza contagem de tempo
    print(f"Tempo total de recepção (UDP): {tempo_fim - tempo_inicio:.6f} segundos")


if __name__ == "__main__":
    servidor_udp()
