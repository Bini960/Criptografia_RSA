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
    ("mensaje", "Mensaje M", 0, 0, 3),
    ("con_relleno", "Mensaje con relleno", 1, 0, 3),
    ("n", "n", 2, 0, 1),
    ("phi", "φ", 2, 1, 1),
    ("mcd", "MCD(e, φ)", 2, 2, 1),
    ("longitud", "Longitud L", 3, 0, 1),
    ("relleno", "Relleno", 3, 1, 1),
    ("llave", "Llave pública (e, n)", 3, 2, 1),
    ("cifrado", "Cifrado C", 4, 0, 3),
]

CAMPOS_DE_SOLO_LECTURA = {"mensaje", "con_relleno", "llave", "cifrado"}


class PestanaEncriptar(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master, fg_color="transparent")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)

        formulario = ctk.CTkFrame(self, fg_color="transparent")
        formulario.grid(row=0, column=0, sticky="ew")
        formulario.columnconfigure((0, 1, 2), weight=1)
        self.campo_mensaje = self._crear_campo(formulario, "Mensaje M", fila=0, columna=0, columnas=4)
        self.campo_p = self._crear_campo(formulario, "Primo p", fila=2, columna=0)
        self.campo_q = self._crear_campo(formulario, "Primo q", fila=2, columna=1)
        self.campo_e = self._crear_campo(formulario, "Exponente e", fila=2, columna=2)

        botones = ctk.CTkFrame(formulario, fg_color="transparent")
        botones.grid(row=3, column=3, sticky="e")
        ctk.CTkButton(botones, text="Encriptar", width=110, command=self.encriptar).pack(side="left", padx=(0, 8))
        ctk.CTkButton(botones, text="Limpiar", width=110, command=self.limpiar,
                      fg_color="gray60", hover_color="gray45").pack(side="left")

        self.panel_mensaje = PanelMensaje(self)
        self.panel_mensaje.grid(row=1, column=0, sticky="ew", pady=(8, 4))

        self.valores = {clave: ctk.StringVar(value="") for clave, *_ in DATOS_RESUMEN}
        resumen = ctk.CTkFrame(self, fg_color="transparent")
        resumen.grid(row=2, column=0, sticky="ew")
        resumen.columnconfigure((1, 3, 5), weight=1)
        negrita = ctk.CTkFont(weight="bold")
        for clave, titulo, fila, par, ancho in DATOS_RESUMEN:
            ctk.CTkLabel(resumen, text=titulo, font=negrita, anchor="w").grid(
                row=fila, column=2 * par, sticky="w", padx=(0, 12), pady=2)
            if clave in CAMPOS_DE_SOLO_LECTURA:
                valor = ctk.CTkEntry(resumen, textvariable=self.valores[clave], state="readonly")
            else:
                valor = ctk.CTkLabel(resumen, textvariable=self.valores[clave], anchor="w")
            valor.grid(row=fila, column=2 * par + 1, columnspan=2 * ancho - 1,
                       sticky="ew", padx=(0, 16), pady=2)

        self.tabla = TablaDetalle(self, COLUMNAS)
        self.tabla.grid(row=3, column=0, sticky="nsew", pady=(8, 0))

    def _crear_campo(self, contenedor, titulo: str, fila: int, columna: int, columnas: int = 1):
        ctk.CTkLabel(contenedor, text=titulo, anchor="w").grid(
            row=fila, column=columna, columnspan=columnas, sticky="w", pady=(6, 0))
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
        e, n = resultado.llave_publica

        self.valores["mensaje"].set(texto_visible(resultado.mensaje))
        self.valores["con_relleno"].set(texto_visible(resultado.mensaje_con_relleno))
        self.valores["n"].set(str(parametros.n))
        self.valores["phi"].set(str(parametros.phi))
        self.valores["mcd"].set(str(parametros.mcd_e_phi))
        self.valores["longitud"].set(str(resultado.longitud))
        self.valores["relleno"].set("Sí, un espacio al final" if resultado.tiene_relleno else "No")
        self.valores["llave"].set(f"({e}, {n})")
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
