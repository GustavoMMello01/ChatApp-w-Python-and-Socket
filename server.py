import socket
import threading
import random

def generate_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

def handle_client(client_socket, client_id, client_color):
    while True:
        try:

            message = client_socket.recv(1024).decode('utf-8')

            if not message:
                return
            
            # message_format = f"Cliente {client_id}: {message}"
            print(f"Broadcasting: {message}")

            for client in clients:
                if client != client_socket:
                    client.send(message.encode('utf-8'))

        except:
            break

    # fecha a conexão   
    client_socket.close()
    clients.remove(client_socket)



def start_server():
    # criando o objeto socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bindando o socket a um endereço e porta
    server_socket.bind(('localhost', 9999))

    # habilitando o socket a aceitar conexões -> modo escuta
    server_socket.listen(5)

    print('Server listening on port 9999')

    client_id = 0

    while True:

        client_socket, addr = server_socket.accept()
        client_id += 1

        client_color = generate_color()

        print(f"Conexão realizada no {addr} para o cliente de ID {client_id} com a cor {client_color}")

        client_socket.send(f"{client_id}|{client_color}".encode('utf-8'))
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket, client_id, client_color)).start()


        pass

clients = []
if __name__ == "__main__":
    start_server()