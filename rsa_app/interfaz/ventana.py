import customtkinter as ctk


class Ventana(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Criptografía RSA")
        self.geometry("1000x700")
        self.minsize(900, 600)

        cuadro = ctk.CTkFrame(self, corner_radius=0, fg_color="gray86")
        cuadro.pack(fill="both", expand=True, padx=15, pady=15)

        barra = ctk.CTkFrame(cuadro, corner_radius=0, fg_color="transparent")
        barra.pack(side="bottom")

        self.marco_encriptar = ctk.CTkFrame(cuadro, corner_radius=0, fg_color="transparent")
        self.marco_desencriptar = ctk.CTkFrame(cuadro, corner_radius=0, fg_color="transparent")

        self.boton_encriptar = ctk.CTkButton(barra, text="Encriptar", width=170, height=40, corner_radius=0,
                                             font=ctk.CTkFont(size=16), text_color="white",
                                             command=self.mostrar_encriptar)
        self.boton_encriptar.pack(side="left")

        self.boton_desencriptar = ctk.CTkButton(barra, text="Desencriptar", width=170, height=40, corner_radius=0,
                                                font=ctk.CTkFont(size=16), text_color="white",
                                                command=self.mostrar_desencriptar)
        self.boton_desencriptar.pack(side="left")

        self.mostrar_encriptar()

    def mostrar_encriptar(self):
        self.marco_desencriptar.pack_forget()
        self.marco_encriptar.pack(fill="both", expand=True, padx=15, pady=15)
        self.boton_encriptar.configure(fg_color="black", hover_color="black")
        self.boton_desencriptar.configure(fg_color="gray45", hover_color="gray35")

    def mostrar_desencriptar(self):
        self.marco_encriptar.pack_forget()
        self.marco_desencriptar.pack(fill="both", expand=True, padx=15, pady=15)
        self.boton_desencriptar.configure(fg_color="black", hover_color="black")
        self.boton_encriptar.configure(fg_color="gray45", hover_color="gray35")
