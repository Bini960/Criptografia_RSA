import time

from rsa_app.cifrado import desencriptar, encriptar


def rechaza_encriptar(mensaje, p, q, e):
    try:
        encriptar(mensaje, p, q, e)
    except ValueError as error:
        return str(error)
    raise AssertionError("Se aceptó M = " + repr(mensaje) + " con p = " + repr(p[:20]) + ", q = " + repr(q) + ", e = " + repr(e[:20]))


def rechaza_desencriptar(texto_c, texto_l, p, q, e):
    try:
        desencriptar(texto_c, texto_l, p, q, e)
    except ValueError as error:
        return str(error)
    raise AssertionError("Se aceptó C = " + repr(texto_c) + " con L = " + repr(texto_l))


resultado = encriptar("RSA", "367", "373", "17")
assert resultado["n"] == 136891
assert resultado["phi"] == 136152
assert resultado["mcd"] == 1
assert resultado["e"] == 17
assert resultado["longitud"] == 3
assert resultado["relleno"]
assert resultado["texto_con_relleno"] == "RSA "
assert resultado["filas"][0] == [1, '"RS"', "082 083", "082083", "026054"]
assert resultado["filas"][1] == [2, '"A "', "065 032", "065032", "123875"]
assert resultado["cifrado"] == "026054 123875"

resultado = desencriptar("026054 123875", "3", "367", "373", "17")
assert resultado["d"] == 8009
assert resultado["n"] == 136891
assert resultado["phi"] == 136152
assert resultado["texto_recuperado"] == "RSA "
assert resultado["mensaje"] == "RSA"
assert resultado["relleno"]
assert resultado["filas"][0] == [1, "026054", "082083", "082 083", '"RS"']
assert resultado["filas"][1] == [2, "123875", "065032", "065 032", '"A "']

casos = [
    ("RSA", "367", "373", "17", "026054 123875"),
    ("HOLA", "367", "373", "17", "062781 058351"),
    ("Hola Mundo", "367", "373", "17", "109641 028621 013427 063943 072468"),
    ("Abc 123 #$%!", "367", "373", "17", "130029 118236 126442 048663 105570 023238"),
    ("a  b   c", "367", "373", "17", "021860 001245 038557 018758"),
    ("  RSA  ", "367", "373", "17", "038557 026054 123875 038557"),
    ("~", "367", "373", "17", "091705"),
    ("   ", "367", "373", "17", "038557 038557"),
    ("AB ", "367", "373", "17", "117927 038557"),
    ("AB  ", "367", "373", "17", "117927 038557"),
    (" I", "367", "373", "17", "000207"),
    ("~~ }{", "3", "42043", "5", "125886 072565 102788"),
    ("~~ }{", "757", "1321", "13", "920469 956005 217101"),
    ("RSA", "367", "373", "680777", "026054 123875"),
    ("RSA", "367", "373", "136153", "082083 065032"),
]
for mensaje, p, q, e, cifrado_esperado in casos:
    resultado = encriptar(mensaje, p, q, e)
    assert resultado["cifrado"] == cifrado_esperado, mensaje
    assert resultado["longitud"] == len(mensaje), mensaje
    assert resultado["relleno"] == (len(mensaje) % 2 == 1), mensaje
    recuperado = desencriptar(resultado["cifrado"], str(resultado["longitud"]), p, q, e)
    assert recuperado["mensaje"] == mensaje, mensaje

assert desencriptar("026054 123875", "3", "367", "373", "680777")["d"] == 8009
assert desencriptar("082083 065032", "3", "367", "373", "136153")["d"] == 1

resultado = encriptar("Hola, mundo!", "2", "63067", "5")
assert desencriptar(resultado["cifrado"], "12", "2", "63067", "5")["mensaje"] == "Hola, mundo!"

todos = ""
for codigo in range(32, 127):
    todos = todos + chr(codigo)
for p, q, e in [("367", "373", "17"), ("3", "42043", "5"), ("757", "1321", "13"), ("2", "63067", "5"), ("401", "409", "65537")]:
    for mensaje in [todos, todos[1:], "  " + todos + "  ", todos[::-1]]:
        resultado = encriptar(mensaje, p, q, e)
        assert len(resultado["filas"]) == (len(mensaje) + 1) // 2
        for bloque in resultado["cifrado"].split(" "):
            assert len(bloque) == 6
        assert desencriptar(resultado["cifrado"], str(len(mensaje)), p, q, e)["mensaje"] == mensaje

ceros = 0
for primero in range(32, 127):
    for segundo in range(32, 127):
        pareja = chr(primero) + chr(segundo)
        cifrado = encriptar(pareja, "367", "373", "17")["cifrado"]
        if cifrado[0] == "0":
            ceros = ceros + 1
        assert desencriptar(cifrado, "2", "367", "373", "17")["mensaje"] == pareja
assert ceros > 0

e_grande = str(17 + 10 ** 4290 * 136152)
assert len(e_grande) == 4296
inicio = time.time()
assert encriptar("RSA", "367", "373", e_grande)["cifrado"] == "026054 123875"
assert desencriptar("026054 123875", "3", "367", "373", e_grande)["mensaje"] == "RSA"
assert time.time() - inicio < 5

rechazos_llave = [
    ("361", "373", "17"),
    ("367", "367", "17"),
    ("47", "71", "17"),
    ("1009", "1013", "17"),
    ("2", "63063", "17"),
    ("1000000000000000000000000000057", "373", "17"),
    ("1", "200003", "17"),
    ("abc", "373", "17"),
    ("3.5", "373", "17"),
    ("١٧", "373", "17"),
    ("1_000", "373", "17"),
    ("", "373", "17"),
    (" 367", "373", "17"),
    ("367 ", "373", "17"),
    ("9" * 4301, "373", "17"),
    ("367", "", "17"),
    ("367", "373", ""),
    ("367", "373", "1"),
    ("367", "373", "0"),
    ("367", "373", "-5"),
    ("367", "373", "2"),
    ("367", "373", "3"),
    ("367", "373", "9"),
    ("367", "373", "+17"),
    ("367", "373", "1" * 4301),
]
for p, q, e in rechazos_llave:
    inicio = time.time()
    rechaza_encriptar("RSA", p, q, e)
    rechaza_desencriptar("026054 123875", "3", p, q, e)
    assert time.time() - inicio < 2

for mensaje, codigo, posicion in [("Señor", 241, 3), ("canción", 243, 6), ("RS\tA", 9, 3), ("RS\nA", 10, 3), ("RSA\r", 13, 4)]:
    error = rechaza_encriptar(mensaje, "367", "373", "17")
    assert str(codigo) in error, error
    assert str(posicion) in error, error
rechaza_encriptar("", "367", "373", "17")

rechazos_cifrado = [
    ("02605 123875", "3"),
    ("0260541 123875", "3"),
    ("02605a 123875", "3"),
    ("026054,123875", "3"),
    ("026054  123875", "3"),
    (" 026054 123875", "3"),
    ("026054 123875 ", "3"),
    ("026054\t123875", "3"),
    ("136891", "2"),
    ("999999", "2"),
    ("", "3"),
    ("026054 123875", "2"),
    ("026054 123875", "5"),
    ("026054 123875", "0"),
    ("026054 123875", "x"),
    ("026054 123875", ""),
    ("026054 123875", " 3"),
    ("117927 100771", "3"),
    ("000000", "2"),
    ("000005", "2"),
]
for texto_c, texto_l in rechazos_cifrado:
    error = rechaza_desencriptar(texto_c, texto_l, "367", "373", "17")
    assert len(error) < 300, error

rechaza_desencriptar("026054 123875", "3", "367", "373", "5")
rechaza_desencriptar("026054 123875", "3" * 4400, "367", "373", "17")

print("Pruebas de cifrado.py superadas.")
