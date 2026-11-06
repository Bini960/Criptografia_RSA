import customtkinter as ctk

from rsa_app import cifrado, codificacion
from rsa_app.interfaz.componentes import PanelMensaje, TablaDetalle, texto_visible
from rsa_app.modelos import ErrorValidacion, ResultadoEncriptacion

COLUMNAS = [
    ("numero", "#"),
    ("pareja", "Pareja"),
    ("codigos", "Códigos ASCII"),
    ("m", "Bloque m (antes)"),
    ("c", "Bloque c (después)"),
]

DATOS_RESUMEN = [
    ("mensaje", "Mensaje M"),
    ("n", "n"),
    ("phi", "φ"),
    ("mcd", "MCD(e, φ)"),
    ("llave", "Llave pública (e, n)"),
    ("longitud", "Longitud L"),
    ("relleno", "Relleno"),
    ("cifrado", "Cifrado C"),
]


class PestanaEncriptar(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master, fg_color="transparent")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(4, weight=1)

        formulario = ctk.CTkFrame(self, fg_color="transparent")
        formulario.grid(row=0, column=0, sticky="ew")
        formulario.columnconfigure((0, 1, 2), weight=1)
        self.campo_mensaje = self._crear_campo(formulario, "Mensaje M", fila=0, columna=0, columnas=3)
        self.campo_p = self._crear_campo(formulario, "Primo p", fila=2, columna=0)
        self.campo_q = self._crear_campo(formulario, "Primo q", fila=2, columna=1)
        self.campo_e = self._crear_campo(formulario, "Exponente e", fila=2, columna=2)

        botones = ctk.CTkFrame(self, fg_color="transparent")
        botones.grid(row=1, column=0, sticky="w", pady=(10, 0))
        ctk.CTkButton(botones, text="Encriptar", command=self.encriptar).pack(side="left", padx=(0, 10))
        ctk.CTkButton(botones, text="Limpiar", command=self.limpiar,
                      fg_color="gray60", hover_color="gray45").pack(side="left")

        self.panel_mensaje = PanelMensaje(self)
        self.panel_mensaje.grid(row=2, column=0, sticky="ew", pady=10)

        self.valores = {clave: ctk.StringVar(value="") for clave, _ in DATOS_RESUMEN}
        resumen = ctk.CTkFrame(self, fg_color="transparent")
        resumen.grid(row=3, column=0, sticky="ew")
        resumen.columnconfigure(1, weight=1)
        negrita = ctk.CTkFont(weight="bold")
        for fila, (clave, titulo) in enumerate(DATOS_RESUMEN):
            ctk.CTkLabel(resumen, text=titulo, font=negrita, anchor="w").grid(
                row=fila, column=0, sticky="w", padx=(0, 16), pady=2)
            if clave == "cifrado":
                valor = ctk.CTkEntry(resumen, textvariable=self.valores[clave], state="readonly")
            else:
                valor = ctk.CTkLabel(resumen, textvariable=self.valores[clave], anchor="w", justify="left")
            valor.grid(row=fila, column=1, sticky="ew", pady=2)

        self.tabla = TablaDetalle(self, COLUMNAS)
        self.tabla.grid(row=4, column=0, sticky="nsew", pady=(10, 0))

    def _crear_campo(self, contenedor, titulo: str, fila: int, columna: int, columnas: int = 1):
        ctk.CTkLabel(contenedor, text=titulo, anchor="w").grid(
            row=fila, column=columna, columnspan=columnas, sticky="w", pady=(8, 0))
        campo = ctk.CTkEntry(contenedor)
        campo.grid(row=fila + 1, column=columna, columnspan=columnas, sticky="ew", padx=(0, 10))
        return campo

    def encriptar(self) -> None:
        self._limpiar_resultado()
        try:
            resultado = cifrado.encriptar(
                self.campo_mensaje.get(),
                self.campo_p.get(),
                self.campo_q.get(),
                self.campo_e.get(),
            )
        except ErrorValidacion as error:
            self.panel_mensaje.mostrar_error(str(error))
            return
        except Exception as error:
            self.panel_mensaje.mostrar_error(f"Ocurrió un error inesperado al encriptar: {error}")
            return
        self._mostrar_resultado(resultado)

    def limpiar(self) -> None:
        for campo in (self.campo_mensaje, self.campo_p, self.campo_q, self.campo_e):
            campo.delete(0, "end")
        self._limpiar_resultado()

    def _limpiar_resultado(self) -> None:
        self.panel_mensaje.limpiar()
        for variable in self.valores.values():
            variable.set("")
        self.tabla.limpiar()

    def _mostrar_resultado(self, resultado: ResultadoEncriptacion) -> None:
        parametros = resultado.parametros
        if resultado.tiene_relleno:
            relleno = f"Sí, se agregó un espacio al final: {texto_visible(resultado.mensaje_con_relleno)}"
        else:
            relleno = "No"

        self.valores["mensaje"].set(texto_visible(resultado.mensaje))
        self.valores["n"].set(str(parametros.n))
        self.valores["phi"].set(str(parametros.phi))
        self.valores["mcd"].set(str(parametros.mcd_e_phi))
        self.valores["llave"].set(f"({resultado.llave_publica[0]}, {resultado.llave_publica[1]})")
        self.valores["longitud"].set(str(resultado.longitud))
        self.valores["relleno"].set(relleno)
        self.valores["cifrado"].set(resultado.cifrado)

        self.tabla.mostrar([
            (
                str(fila.numero),
                f'"{fila.pareja}"',
                f"{fila.codigos[0]:03d} {fila.codigos[1]:03d}",
                codificacion.formatear_bloque(fila.bloque_m),
                codificacion.formatear_bloque(fila.bloque_c),
            )
            for fila in resultado.filas
        ])
