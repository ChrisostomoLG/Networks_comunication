import socket
import time


def tcp_client(nome_arquivo, host='localhost', port=5001):
    tempo_inicio = time.time()  # Inicia contagem de tempo

    with open(nome_arquivo, 'rb') as f:
        conteudo_arquivo = f.read()

    socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_cliente.connect((host, port))

    # Envia o tamanho do arquivo
    tamanho_arquivo = len(conteudo_arquivo)
    socket_cliente.sendall(tamanho_arquivo.to_bytes(8, byteorder='big'))

    # Envia os dados do arquivo em pedaços de até 1024 bytes
    bytes_enviados = 0
    while bytes_enviados < tamanho_arquivo:
        batelada = conteudo_arquivo[bytes_enviados:bytes_enviados + 1024]
        socket_cliente.sendall(batelada)
        bytes_enviados += len(batelada)
    # Fecha a conexão ao enviar o arquivo.
    socket_cliente.close()

    tempo_fim = time.time()  # Finaliza contagem de tempo
    print(f"Tempo de transmissão (TCP): {tempo_fim - tempo_inicio:.6f} segundos")


if __name__ == "__main__":
    tcp_client('arquivocomtexto.txt')