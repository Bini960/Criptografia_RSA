def agregar_relleno(mensaje):
    if len(mensaje) % 2 == 0:
        return mensaje
    else:
        return mensaje + " "

def pareja_a_numero(pareja):
    codigo1 = ord(pareja[0])
    codigo2 = ord(pareja[1])

    bloque1 = str(codigo1).zfill(3)
    bloque2 = str(codigo2).zfill(3)

    return int(bloque1 + bloque2)

def numero_a_codigos(numero):
    bloque_texto = str(numero).zfill(6)
    bloque1 = bloque_texto[0:3]
    bloque2 = bloque_texto[3:6]
    return (int(bloque1), int(bloque2))

def codigos_a_pareja(codigo1, codigo2):
    caracter1 = chr(codigo1)
    caracter2 = chr(codigo2)
    pareja = caracter1 + caracter2
    return pareja

def unir_bloques(bloques):
    lista_textos = []
    
    for bloque in bloques:
        bloque_texto = str(bloque).zfill(6)
        lista_textos.append(bloque_texto)
    
    return " ".join(lista_textos)

def quitar_relleno(texto, longitud):
    if longitud % 2 != 0:
        return texto[:-1]
    else:
        return texto