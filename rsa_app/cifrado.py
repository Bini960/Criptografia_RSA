from rsa_app import codificacion, matematica, validacion
from rsa_app.modelos import FilaBloque, ResultadoDesencriptacion, ResultadoEncriptacion


def encriptar(mensaje: str, texto_p: str, texto_q: str, texto_e: str) -> ResultadoEncriptacion:
    parametros = validacion.validar_parametros(texto_p, texto_q, texto_e)
    mensaje = validacion.validar_mensaje(mensaje)

    longitud = len(mensaje)
    texto, tiene_relleno = codificacion.aplicar_relleno(mensaje)

    filas = []
    for inicio in range(0, len(texto), 2):
        pareja = texto[inicio:inicio + 2]
        codigos, bloque_m = codificacion.pareja_a_bloque(pareja)
        bloque_c = matematica.exponenciacion_modular(bloque_m, parametros.e, parametros.n)
        filas.append(FilaBloque(
            numero=inicio // 2 + 1,
            pareja=pareja,
            codigos=codigos,
            bloque_m=bloque_m,
            bloque_c=bloque_c,
        ))

    cifrado = codificacion.formatear_cifrado([fila.bloque_c for fila in filas])

    return ResultadoEncriptacion(
        parametros=parametros,
        mensaje=mensaje,
        longitud=longitud,
        tiene_relleno=tiene_relleno,
        filas=tuple(filas),
        cifrado=cifrado,
    )


def desencriptar(texto_c: str, texto_l: str, texto_p: str, texto_q: str,
                 texto_e: str) -> ResultadoDesencriptacion:
    parametros = validacion.validar_parametros(texto_p, texto_q, texto_e)
    bloques_c = validacion.validar_cifrado(texto_c, parametros.n)
    longitud = validacion.validar_longitud(texto_l, len(bloques_c))

    d = matematica.inverso_modular(parametros.e, parametros.phi)

    filas = []
    for numero, bloque_c in enumerate(bloques_c, start=1):
        bloque_m = matematica.exponenciacion_modular(bloque_c, d, parametros.n)
        codigos = codificacion.bloque_a_codigos(bloque_m)
        validacion.validar_codigos(codigos, numero)
        filas.append(FilaBloque(
            numero=numero,
            pareja=codificacion.codigos_a_pareja(codigos),
            codigos=codigos,
            bloque_m=bloque_m,
            bloque_c=bloque_c,
        ))

    texto_recuperado = "".join(fila.pareja for fila in filas)
    validacion.validar_relleno(texto_recuperado, longitud)
    mensaje = codificacion.quitar_relleno(texto_recuperado, longitud)

    return ResultadoDesencriptacion(
        parametros=parametros,
        d=d,
        longitud=longitud,
        tiene_relleno=longitud % 2 == 1,
        filas=tuple(filas),
        texto_recuperado=texto_recuperado,
        mensaje=mensaje,
    )
