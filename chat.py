import socket
import threading
import customtkinter as ctk

class ChatApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Chat Application")  # Título da janela
        self.geometry("400x400")  # Tamanho da janela

        # Frame para a área de chat
        self.chat_frame = ctk.CTkFrame(self)
        self.chat_frame.pack(fill='both', expand=True)

        # Área de texto para exibir mensagens
        self.chat_area = ctk.CTkTextbox(self.chat_frame, state='disabled')
        self.chat_area.pack(padx=10, pady=10, fill='both', expand=True)

        # Campo de entrada para mensagens
        self.entry = ctk.CTkEntry(self, placeholder_text="Enter your message")
        self.entry.pack(padx=10, pady=5, fill='x')

        # Botão para enviar mensagens
        self.send_button = ctk.CTkButton(self, text="Send", command=self.send_message)
        self.send_button.pack(padx=10, pady=5)

        # Configuração do socket do cliente
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('localhost', 12345))  # Conecta ao servidor

        # Recebe o ID do cliente do servidor
        self.client_id = self.client_socket.recv(1024).decode('utf-8')
        # recebe o ID do cliente do servidor e o decodifica de bytes para string.
        print(f"Assigned ID: {self.client_id}")

        # Inicia uma thread para receber mensagens
        threading.Thread(target=self.receive_messages, daemon=True).start()
        # threading.Thread é uma classe que representa uma thread de execução separada.
        # target é a função que será executada na thread.
        # daemon=True faz com que a thread seja encerrada quando o programa principal terminar.

    def send_message(self):
        # Envia a mensagem digitada para o servidor
        message = self.entry.get()
        if message:
            formatted_message = f"{self.client_id}: {message}"
            self.client_socket.send(formatted_message.encode('utf-8'))
            self.entry.delete(0, 'end')  # Limpa o campo de entrada
            # Adiciona a mensagem à área de chat local
            self.chat_area.configure(state='normal')
            self.chat_area.insert('end', f"You ({self.client_id}): {message}\n")
            self.chat_area.configure(state='disabled')
            self.chat_area.yview('end')  # Rola para o final

    def receive_messages(self):
        # Recebe mensagens do servidor e as exibe na área de chat
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                self.chat_area.configure(state='normal')
                self.chat_area.insert('end', message + '\n')
                self.chat_area.configure(state='disabled')
                self.chat_area.yview('end')  # Rola para o final
            except:
                break

if __name__ == "__main__":
    app = ChatApp()  # Cria a aplicação de chat
    app.mainloop()  # Inicia a interface gráfica