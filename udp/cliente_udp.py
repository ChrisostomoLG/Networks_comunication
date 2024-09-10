import socket
import time
import zlib


def cliente_udp(filename, host='localhost', port=5002):
    tempo_inicio = time.time()  # Inicia contagem de tempo

    socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    with open(filename, 'rb') as f:
        conteudo_arquivo = f.read()

    # Envia o tamanho do arquivo
    tamanho_arquivo = len(conteudo_arquivo)
    socket_cliente.sendto(tamanho_arquivo.to_bytes(8, byteorder='big'), (host, port))

    # Envia os dados do arquivo em pacotes de até 1024 bytes
    bytes_enviados = 0
    while bytes_enviados < tamanho_arquivo:
        batelada = conteudo_arquivo[bytes_enviados:bytes_enviados + 1024]
        checksum = zlib.crc32(batelada)
        # Envia o checksum (4 bytes) seguido pelo chunk de dados
        socket_cliente.sendto(checksum.to_bytes(4, byteorder='big') + batelada, (host, port))
        bytes_enviados += len(batelada)

    socket_cliente.close()

    tempo_final = time.time()  # Finaliza contagem de tempo
    print(f"Tempo de transmissão (UDP): {tempo_final - tempo_inicio:.6f} segundos")


if __name__ == "__main__":
    cliente_udp('arquivocomtexto.txt')