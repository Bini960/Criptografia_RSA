from dataclasses import dataclass


class ErrorValidacion(ValueError):
    pass


@dataclass(frozen=True)
class ParametrosRSA:
    p: int
    q: int
    e: int
    n: int
    phi: int
    mcd_e_phi: int


@dataclass(frozen=True)
class FilaBloque:
    numero: int
    pareja: str
    codigos: tuple[int, int]
    bloque_m: int
    bloque_c: int


@dataclass(frozen=True)
class ResultadoEncriptacion:
    parametros: ParametrosRSA
    mensaje: str
    longitud: int
    tiene_relleno: bool
    filas: tuple[FilaBloque, ...]
    cifrado: str

    @property
    def llave_publica(self) -> tuple[int, int]:
        return (self.parametros.e, self.parametros.n)

    @property
    def mensaje_con_relleno(self) -> str:
        return self.mensaje + " " if self.tiene_relleno else self.mensaje


@dataclass(frozen=True)
class ResultadoDesencriptacion:
    parametros: ParametrosRSA
    d: int
    longitud: int
    tiene_relleno: bool
    filas: tuple[FilaBloque, ...]
    texto_recuperado: str
    mensaje: str

    @property
    def llave_privada(self) -> tuple[int, int]:
        return (self.d, self.parametros.n)
