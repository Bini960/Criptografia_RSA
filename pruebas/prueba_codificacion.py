from rsa_app.codificacion import agregar_relleno, codigos_a_pareja, numero_a_codigos, pareja_a_numero, quitar_relleno, unir_bloques


def codificar(mensaje):
    texto = agregar_relleno(mensaje)
    bloques = []
    for i in range(0, len(texto), 2):
        bloques.append(pareja_a_numero(texto[i:i + 2]))
    return unir_bloques(bloques)


def decodificar(texto_bloques, longitud):
    recuperado = ""
    for parte in texto_bloques.split(" "):
        codigo1, codigo2 = numero_a_codigos(int(parte))
        recuperado = recuperado + codigos_a_pareja(codigo1, codigo2)
    return quitar_relleno(recuperado, longitud)


assert agregar_relleno("RSA") == "RSA "
assert agregar_relleno("HOLA") == "HOLA"
assert agregar_relleno("A") == "A "
assert agregar_relleno("  RSA  ") == "  RSA   "
assert agregar_relleno("AB  ") == "AB  "
assert agregar_relleno(" ") == "  "

assert pareja_a_numero("AB") == 65066
assert pareja_a_numero("RS") == 82083
assert pareja_a_numero(" I") == 32073
assert pareja_a_numero("A ") == 65032
assert pareja_a_numero("  ") == 32032
assert pareja_a_numero("~~") == 126126

assert numero_a_codigos(82083) == (82, 83)
assert numero_a_codigos(5) == (0, 5)
assert numero_a_codigos(32073) == (32, 73)
assert numero_a_codigos(126126) == (126, 126)
assert numero_a_codigos(0) == (0, 0)

assert codigos_a_pareja(82, 83) == "RS"
assert codigos_a_pareja(65, 32) == "A "
assert codigos_a_pareja(32, 73) == " I"

assert unir_bloques([26054, 123875]) == "026054 123875"
assert unir_bloques([82083, 65032]) == "082083 065032"
assert unir_bloques([5]) == "000005"
assert unir_bloques([0, 999999, 12]) == "000000 999999 000012"

assert quitar_relleno("RSA ", 3) == "RSA"
assert quitar_relleno("  RSA   ", 7) == "  RSA  "
assert quitar_relleno("AB  ", 4) == "AB  "
assert quitar_relleno("HOLA", 4) == "HOLA"
assert quitar_relleno("~ ", 1) == "~"
assert quitar_relleno("   ", 3) == "  "

for codigo1 in range(32, 127):
    for codigo2 in range(32, 127):
        pareja = codigos_a_pareja(codigo1, codigo2)
        assert numero_a_codigos(pareja_a_numero(pareja)) == (codigo1, codigo2), (codigo1, codigo2)

assert codificar("RSA") == "082083 065032"
assert codificar("HOLA") == "072079 076065"
assert codificar("AB  ") == "065066 032032"

mensajes = ["RSA", "HOLA", "~", " ", "   ", "  RSA  ", "a  b   c", "Hola Mundo", "AB ", "AB  ", "Abc 123 #$%!", "~~ }{"]
for mensaje in mensajes:
    assert decodificar(codificar(mensaje), len(mensaje)) == mensaje, mensaje

print("Pruebas de codificacion.py superadas.")