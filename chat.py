import customtkinter as ctk
import socket
import threading

class ChatApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Chat Socket")
        self.geometry("400x400")


        self.chat_frame = ctk.CTkFrame(self)
        self.chat_frame.pack(fill="both", expand=True)

        # Textbox onde ficam as mensagens
        self.chat_text = ctk.CTkTextbox(self.chat_frame, state="disabled", wrap="word")
        self.chat_text.pack(padx=10, pady=10, fill="both", expand=True)

        # Campo de entrada para as mensagens do usuario
        self.entry = ctk.CTkEntry(self, placeholder_text = "Digite sua mensagem")
        self.entry.pack(fill="x", padx=10, pady=10)

        # Botão para enviar a mensagem
        self.send_btn = ctk.CTkButton(self, text="Enviar", command=self.send_message)
        self.send_btn.pack(fill="x", padx=10, pady=15)
        
        # Inicializando o socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('localhost', 9999))

        # Recebendo o ID do cliente e a cor
        self.client_id, self.client_color = self.client_socket.recv(1024).decode('utf-8').split("|")
        print(f"Cliente conectado com ID {self.client_id} e cor {self.client_color}")

        # Inicializando a thread para receber mensagens
        threading.Thread(target=self.receive_message, daemon=True).start()




    
    def send_message(self):
        message = self.entry.get() 
        
        if message:
            message_format = f"{self.client_id}|{self.client_color}|{message}"

            self.client_socket.send(message_format.encode('utf-8'))
            self.entry.delete(0, "end")

            self.display_message(f"You ({self.client_id}): {message}", self.client_color)



    def receive_message(self):
        while True:
            try:
                # conversar com o socket para receber a mensagem
                message = self.client_socket.recv(1024).decode('utf-8')
                client_id, client_color, message = message.split("|")

                self.display_message(f"{client_id}: {message}", client_color)


            except:
                break
    def display_message(self, message, color):

        # inserir a mensagem no chat_text 
        self.chat_text.configure(state="normal")
        self.chat_text.insert("end", message + "\n")

        tag_name = f"{color}_tag"
        self.chat_text.tag_add(tag_name, 'end-2l', 'end-1c')
        self.chat_text.tag_config(tag_name, foreground=color)
        
        self.chat_text.configure(state="disabled")
        self.chat_text.yview("end")


if __name__ == "__main__":
    app = ChatApp()
    app.mainloop()