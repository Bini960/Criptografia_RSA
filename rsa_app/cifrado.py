import sys
from rsa_app.codificacion import agregar_relleno, codigos_a_pareja, numero_a_codigos, pareja_a_numero, quitar_relleno, unir_bloques
from rsa_app.validacion import validar_cifrado, validar_codigos, validar_llave, validar_longitud, validar_mensaje, validar_relleno
from rsa_app.matematica import exponenciacion_modular, inverso_modular, mcd_euclides
sys.setrecursionlimit(20000)

def encriptar(mensaje, texto_p, texto_q, texto_e):
    p, q, e, n, phi  = validar_llave(texto_p, texto_q, texto_e)
    validar_mensaje(mensaje)

    longitud = len(mensaje)
    texto_relleno = agregar_relleno(mensaje)

    relleno = longitud != len(texto_relleno)

    bloques_cifrados = []
    filas= []

    for i in range(0, len(texto_relleno), 2):
        pareja = texto_relleno[i:i + 2]
        m = pareja_a_numero(pareja)
        c = exponenciacion_modular(m, e, n)
        bloques_cifrados.append(c)

        codigo1 = str(ord(pareja[0])).zfill(3)
        codigo2 = str(ord(pareja[1])).zfill(3)
        fila = [i // 2 + 1, '"' + pareja + '"', codigo1 + " " + codigo2, str(m).zfill(6), str(c).zfill(6)]
        filas.append(fila)

    cifrado = unir_bloques(bloques_cifrados)
    mcd = mcd_euclides(e, phi)

    return {"mensaje": mensaje, "texto_con_relleno": texto_relleno, "longitud": longitud, "relleno": relleno, "e": e, "n": n, "phi": phi, "mcd": mcd, "cifrado": cifrado, "filas": filas}

def desencriptar(texto_c, texto_l, texto_p, texto_q, texto_e):
    p, q, e, n, phi = validar_llave(texto_p, texto_q, texto_e)
    bloques_cifrados = validar_cifrado(texto_c, n)
    longitud = validar_longitud(texto_l, len(bloques_cifrados))

    d = inverso_modular(e, phi)

    texto_recuperado = ""
    filas = []

    for i in range(len(bloques_cifrados)):
        c = bloques_cifrados[i]
        numero_bloque = i + 1

        if c == 0:
            m = 0
        else:
            m = exponenciacion_modular(c, d, n)

        codigo1, codigo2 = numero_a_codigos(m)
        validar_codigos(codigo1, codigo2, numero_bloque)
        pareja = codigos_a_pareja(codigo1, codigo2)
        texto_recuperado = texto_recuperado + pareja

        codigos = str(codigo1).zfill(3) + " " + str(codigo2).zfill(3)
        fila = [numero_bloque, str(c).zfill(6), str(m).zfill(6), codigos, '"' + pareja + '"']
        filas.append(fila)

    validar_relleno(texto_recuperado, longitud)
    mensaje = quitar_relleno(texto_recuperado, longitud)
    relleno = longitud % 2 != 0

    return {"texto_recuperado": texto_recuperado, "mensaje": mensaje, "longitud": longitud, "relleno": relleno, "d": d, "n": n, "phi": phi, "filas": filas}