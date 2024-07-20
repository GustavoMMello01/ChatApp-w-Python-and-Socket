import customtkinter as ctk

class Toolbar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, height=30, fg_color="blue")
        
        self.label = ctk.CTkLabel(self, text="Toolbar Teste", text_color="white", font=("Arial", 8))
        self.label.pack(padx=1, pady=1, fill="x", expand=True)

class Footer(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, height=30, fg_color="blue")
        
        self.label = ctk.CTkLabel(self, text="2024 - Footer Teste", text_color="white", font=("Arial", 8))
        self.label.pack(padx=1, pady=1, fill="x", expand=True)

class View1(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        self.controller = controller
        
        self.label = ctk.CTkLabel(self, text="View 1", font=("Arial", 12))
        self.label.pack(padx=10, pady=10)
        
        self.entry1 = ctk.CTkEntry(self, placeholder_text="Enter number")
        self.entry1.pack(padx=10, pady=5)
        
        self.entry2 = ctk.CTkEntry(self, placeholder_text="Enter another number")
        self.entry2.pack(padx=10, pady=5)
        
        self.result_label = ctk.CTkLabel(self, text="Result: ", font=("Arial", 12))
        self.result_label.pack(padx=10, pady=5)
        
        self.add_button = ctk.CTkButton(self, text="Add Numbers", command=self.add_numbers)
        self.add_button.pack(padx=10, pady=5)
    
    def add_numbers(self):
        try:
            num1 = float(self.entry1.get())
            num2 = float(self.entry2.get())
            result = num1 + num2
            self.result_label.configure(text=f"Result: {result}")
        except ValueError:
            self.result_label.configure(text="Invalid input. Please enter valid numbers.")

class AppController(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Aplicativo Teste")
        self.geometry("400x400")

        self.toolbar = Toolbar(self)
        self.toolbar.pack(side=ctk.TOP, fill=ctk.X)

        self.view1 = View1(self, self)
        self.view1.pack(fill='both', expand=True)

        self.footer = Footer(self)
        self.footer.pack(side=ctk.BOTTOM, fill=ctk.X)

if __name__ == "__main__":
    app = AppController()
    app.mainloop()
