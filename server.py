import socket
import threading

def handle_client(client_socket, client_id):
    # Função para lidar com um cliente específico
    while True:
        try:
            # Recebe a mensagem do cliente
            message = client_socket.recv(1024).decode('utf-8')
            # recv recebe os dados do socket. O argumento 1024 especifica o número máximo de bytes a serem recebidos.
            # recv é uma chamada de sistema bloqueante, o que significa que o 
            # programa ficará parado até que os dados sejam recebidos.
            
            # Se a mensagem estiver vazia, encerra o loop
            if not message:
                break
            # Formata a mensagem para incluir o ID do cliente
            formatted_message = f"{client_id}: {message}"
            print(f"Broadcasting: {formatted_message}")  #um método de transferência de 
                                                #mensagem para todos os receptores simultaneamente.
            # Envia a mensagem formatada para todos os clientes, exceto o remetente
            for client in clients:
                if client != client_socket:
                    client.send(formatted_message.encode('utf-8'))
        except:
            break
    # Fecha a conexão e remove o cliente da lista de clientes
    client_socket.close()
    clients.remove(client_socket)

def start_server():
    # Cria um OBJETO socket para o servidor
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # socket.AF_INET: Especifica a família de endereços do socket. 
    # AF_INET significa que usaremos IPv4 (endereços IP de 4 bytes, como 192.168.0.1).

    # socket.SOCK_STREAM: Especifica o tipo de socket. 
    # SOCK_STREAM significa que usaremos um socket TCP (Transmission Control Protocol).


    # Liga o socket à porta 12345
    server_socket.bind(('localhost', 12345))
    
    # Coloca o servidor em modo de escuta
    server_socket.listen(5)
    # O argumento 5 especifica o número máximo de conexões pendentes na fila de conexões.
    print("Server listening on port 12345")

    client_id_counter = 1  # Contador de IDs de clientes

    while True:
        # Aceita uma nova conexão
        client_socket, addr = server_socket.accept()
        client_id = client_id_counter  # Atribui um ID ao cliente
        client_id_counter += 1  # Incrementa o contador de IDs
        print(f"Connection from {addr}, assigned ID {client_id}")
        # Envia o ID ao cliente
        client_socket.send(str(client_id).encode('utf-8'))
        # Adiciona o cliente à lista de clientes
        clients.append(client_socket)
        # Inicia uma nova thread para lidar com o cliente
        threading.Thread(target=handle_client, args=(client_socket, client_id)).start()
        # target é a função que será executada pela thread.
        # O argumento args é uma tupla contendo os argumentos que serão passados para a função handle_client.

clients = []  # Lista para armazenar os clientes conectados
if __name__ == "__main__":
    start_server()  # Inicia o servidor
