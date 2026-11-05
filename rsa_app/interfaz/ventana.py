import customtkinter as ctk

TITULO = "Criptografía RSA · MM2015 Matemática Discreta 1"


class VentanaPrincipal(ctk.CTk):
    def __init__(self) -> None:
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        super().__init__()

        self.title(TITULO)
        self.geometry("1100x720")
        self.minsize(900, 600)

        self.pestanas = ctk.CTkTabview(self)
        self.pestanas.pack(fill="both", expand=True, padx=16, pady=16)
        self.pestanas.add("Encriptar")
        self.pestanas.add("Desencriptar")
