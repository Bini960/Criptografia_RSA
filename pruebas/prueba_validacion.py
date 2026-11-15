from rsa_app.validacion import leer_entero, validar_cifrado, validar_codigos, validar_llave, validar_longitud, validar_mensaje, validar_relleno


def lanza_error(funcion, *argumentos):
    try:
        funcion(*argumentos)
    except ValueError:
        return True
    return False


assert leer_entero("367", "p") == 367
assert leer_entero("007", "p") == 7
assert leer_entero("0", "e") == 0
assert leer_entero("1" * 4300, "p") == int("1" * 4300)
for texto in ["", "12a", " 5", "5 ", "-3", "+7", "1.5", "1_000", "٣", "1" * 4301]:
    assert lanza_error(leer_entero, texto, "p"), texto

assert validar_llave("367", "373", "17") == (367, 373, 17, 136891, 136152)
assert validar_llave("367", "373", "680777") == (367, 373, 680777, 136891, 136152)
assert validar_llave("367", "373", "136153") == (367, 373, 136153, 136891, 136152)
assert validar_llave("3", "42043", "5") == (3, 42043, 5, 126129, 84084)
assert validar_llave("757", "1321", "13") == (757, 1321, 13, 999997, 997920)
assert validar_llave("2", "63067", "5") == (2, 63067, 5, 126134, 63066)
casos_llave = [
    ("367", "367", "17"),
    ("2", "3", "17"),
    ("2", "63063", "17"),
    ("500", "2000", "17"),
    ("1009", "1013", "17"),
    ("361", "373", "17"),
    ("367", "361", "17"),
    ("367", "373", "0"),
    ("367", "373", "1"),
    ("367", "373", "2"),
    ("367", "373", "136152"),
    ("", "373", "17"),
    ("367", "", "17"),
    ("367", "373", ""),
    ("367", "373", "abc"),
    ("0", "373", "17"),
    ("1", "200003", "17"),
    ("1" * 4300, "373", "17"),
]
for texto_p, texto_q, texto_e in casos_llave:
    assert lanza_error(validar_llave, texto_p, texto_q, texto_e), (texto_p, texto_q, texto_e)

for mensaje in ["RSA", "Hola Mundo", " ", "   ", "~", "Abc 123 #$%!", "  RSA  "]:
    assert not lanza_error(validar_mensaje, mensaje), mensaje
texto_completo = ""
for codigo in range(32, 127):
    texto_completo = texto_completo + chr(codigo)
assert not lanza_error(validar_mensaje, texto_completo)
for mensaje in ["", "Año", "ñ", "é", "a\tb", "Hola\n", "a\x7f", "a\x1f"]:
    assert lanza_error(validar_mensaje, mensaje), repr(mensaje)

assert validar_cifrado("026054 123875", 136891) == [26054, 123875]
assert validar_cifrado("000000", 136891) == [0]
assert validar_cifrado("136890", 136891) == [136890]
assert validar_cifrado("000005 000006 000007", 136891) == [5, 6, 7]
for texto_c in ["", " ", "026054  123875", " 026054", "026054 ", "02605", "0260541", "02605a", "026054,123875", "136891", "999999", "026054 12387", "026054 -23875"]:
    assert lanza_error(validar_cifrado, texto_c, 136891), repr(texto_c)

assert validar_longitud("3", 2) == 3
assert validar_longitud("4", 2) == 4
assert validar_longitud("1", 1) == 1
assert validar_longitud("2", 1) == 2
assert validar_longitud("15", 8) == 15
assert validar_longitud("16", 8) == 16
for texto_l, cantidad in [("2", 2), ("5", 2), ("1", 2), ("0", 2), ("", 2), ("3a", 2), ("-3", 2), ("14", 8), ("17", 8), ("6", 4), ("9", 4)]:
    assert lanza_error(validar_longitud, texto_l, cantidad), (texto_l, cantidad)

for codigo1, codigo2 in [(82, 83), (32, 126), (126, 32), (32, 32), (126, 126)]:
    assert not lanza_error(validar_codigos, codigo1, codigo2, 1), (codigo1, codigo2)
for codigo1, codigo2 in [(31, 83), (82, 127), (0, 5), (32, 200), (255, 32), (31, 127), (-1, 50)]:
    assert lanza_error(validar_codigos, codigo1, codigo2, 1), (codigo1, codigo2)

for texto, longitud in [("RSA ", 3), ("HOLA", 4), ("  RSA   ", 7), ("A ", 1), ("AB  ", 4), ("AB", 2)]:
    assert not lanza_error(validar_relleno, texto, longitud), (texto, longitud)
for texto, longitud in [("RSAX", 3), ("RSA", 3), ("A", 1), ("  RSAX", 5)]:
    assert lanza_error(validar_relleno, texto, longitud), (texto, longitud)

print("Pruebas de validacion.py superadas.")