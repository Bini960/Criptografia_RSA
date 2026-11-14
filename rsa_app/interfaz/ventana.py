import customtkinter as ctk


class Ventana(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Criptografía RSA")
        self.geometry("1000x700")
        self.minsize(900, 600)

        pestanas = ctk.CTkTabview(self)
        pestanas.pack(fill="both", expand=True, padx=15, pady=15)
        pestanas.add("Encriptar")
        pestanas.add("Desencriptar")
