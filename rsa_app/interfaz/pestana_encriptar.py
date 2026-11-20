import customtkinter as ctk
from rsa_app.cifrado import encriptar
from rsa_app.interfaz.componentes import Tabla, con_comillas


class PestanaEncriptar(ctk.CTkFrame):
    def __init__(self, contenedor):
        super().__init__(contenedor, fg_color="transparent")

        ctk.CTkLabel(self, text="Mensaje M", anchor="w").pack(fill="x")
        self.campo_mensaje = ctk.CTkEntry(self)
        self.campo_mensaje.pack(fill="x", pady=(0, 10))

        fila = ctk.CTkFrame(self, fg_color="transparent")
        fila.pack(fill="x", pady=(0, 5))

        self.campo_p = self.crear_campo(fila, "p")
        self.campo_q = self.crear_campo(fila, "q")
        self.campo_e = self.crear_campo(fila, "e")

        ctk.CTkButton(fila, text="Limpiar", width=110, corner_radius=0, fg_color="gray45", hover_color="gray35", text_color="white", command=self.limpiar).pack(side="right", anchor="s")
        ctk.CTkButton(fila, text="Encriptar", width=110, corner_radius=0, fg_color="black", hover_color="gray20", text_color="white", command=self.ejecutar).pack(side="right", anchor="s", padx=(0, 10))

        self.etiqueta_error = ctk.CTkLabel(self, text="", text_color="red", anchor="w", justify="left", wraplength=850)
        self.etiqueta_error.pack(fill="x", pady=(0, 5))

        self.resumen = ctk.CTkTextbox(self, height=130)
        self.resumen.configure(state="disabled")
        self.resumen.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(self, text="Mensaje cifrado C", anchor="w").pack(fill="x")
        self.campo_c = ctk.CTkEntry(self, state="readonly")
        self.campo_c.pack(fill="x", pady=(0, 10))

        self.tabla = Tabla(self, ["Número", "Pareja", "Códigos ASCII", "Bloque m (antes)", "Bloque c (después)"])
        self.tabla.pack(fill="both", expand=True)

    def crear_campo(self, fila, nombre):
        columna = ctk.CTkFrame(fila, fg_color="transparent")
        columna.pack(side="left", padx=(0, 10))
        ctk.CTkLabel(columna, text=nombre, anchor="w").pack(fill="x")
        campo = ctk.CTkEntry(columna, width=130)
        campo.pack()
        return campo

    def escribir_resumen(self, texto):
        self.resumen.configure(state="normal")
        self.resumen.delete("1.0", "end")
        self.resumen.insert("1.0", texto)
        self.resumen.configure(state="disabled")

    def escribir_cifrado(self, texto):
        self.campo_c.configure(state="normal")
        self.campo_c.delete(0, "end")
        self.campo_c.insert(0, texto)
        self.campo_c.configure(state="readonly")

    def borrar_resultados(self):
        self.escribir_resumen("")
        self.escribir_cifrado("")
        self.tabla.limpiar()

    def ejecutar(self):
        mensaje = self.campo_mensaje.get()
        texto_p = self.campo_p.get()
        texto_q = self.campo_q.get()
        texto_e = self.campo_e.get()
        try:
            resultado = encriptar(mensaje, texto_p, texto_q, texto_e)
        except ValueError as error:
            self.borrar_resultados()
            self.etiqueta_error.configure(text=str(error))
            return

        self.etiqueta_error.configure(text="")

        if resultado["relleno"]:
            linea_relleno = 'Mensaje con relleno: "' + resultado["texto_con_relleno"] + '"'
        else:
            linea_relleno = "Relleno: No"

        lineas = [
            "Mensaje M: " + con_comillas(resultado["mensaje"]),
            "Longitud L: " + str(resultado["longitud"]),
            linea_relleno,
            "p = " + texto_p + "     q = " + texto_q + "     e = " + texto_e,
            "n = " + str(resultado["n"]) + "     φ = " + str(resultado["phi"]) + "     MCD(e, φ) = " + str(resultado["mcd"]),
            "Llave pública (e, n): (" + str(resultado["e"]) + ", " + str(resultado["n"]) + ")"
        ]
        self.escribir_resumen("\n".join(lineas))
        self.escribir_cifrado(resultado["cifrado"])
        self.tabla.mostrar(resultado["filas"])

    def limpiar(self):
        self.campo_mensaje.delete(0, "end")
        self.campo_p.delete(0, "end")
        self.campo_q.delete(0, "end")
        self.campo_e.delete(0, "end")
        self.etiqueta_error.configure(text="")
        self.borrar_resultados()