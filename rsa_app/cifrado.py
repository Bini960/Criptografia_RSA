import sys
from rsa_app.codificacion import agregar_relleno, pareja_a_numero, unir_bloques
from rsa_app.validacion import validar_llave, validar_mensaje
from rsa_app.matematica import exponenciacion_modular, mcd_euclides
sys.setrecursionlimit(20000)

def encriptar(mensaje, texto_p, texto_q, texto_e):
    p, q, e, n, phi  = validar_llave(texto_p, texto_q, texto_e)
    validar_mensaje(mensaje)

    longitud = len(mensaje)
    texto_relleno = agregar_relleno(mensaje)

    relleno = longitud != len(texto_relleno)

    print(texto_relleno, longitud, relleno)