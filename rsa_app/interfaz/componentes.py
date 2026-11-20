import customtkinter as ctk
from tkinter import ttk


class Tabla(ctk.CTkFrame):
    def __init__(self, contenedor, columnas):
        super().__init__(contenedor)
        self.tabla = ttk.Treeview(self, columns=columnas, show="headings")
        for columna in columnas:
            self.tabla.heading(columna, text=columna)
            self.tabla.column(columna, anchor="w", width=120)

        barra = ttk.Scrollbar(self, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=barra.set)
        self.tabla.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")

    def limpiar(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

    def mostrar(self, filas):
        self.limpiar()
        for fila in filas:
            self.tabla.insert("", "end", values=fila)


def con_comillas(texto):
    if len(texto) == 1:
        return '"' + texto + '" (1 carácter)'
    return '"' + texto + '" (' + str(len(texto)) + " caracteres)"