from rsa_app.matematica import es_primo, mcd_euclides

def leer_entero(texto, nombre):
    if texto == "":
        raise ValueError(f"Falta el valor de {nombre}.")

    for caracter in texto:
        if caracter not in "0123456789":
            raise ValueError(f"El valor de {nombre} debe escribirse solo con dígitos, sin espacios, puntos o signos.")

    if len(texto) > 4300:
        raise ValueError(f"El texto {nombre} es demasiado largo.")

    return int(texto)

def validar_llave(texto_p, texto_q, texto_e):
    p = leer_entero(texto_p, "p")
    q = leer_entero(texto_q, "q")
    e = leer_entero(texto_e, "e")

    if p == q:
        raise ValueError("p no puede ser igual a q.")

    n = p * q
    if n <= 126126 or n >= 1000000:
        raise ValueError("El producto de p y q debe quedar entre 126126 y 1000000.")

    if not es_primo(p):
        raise ValueError("p no es un número primo.")

    if not es_primo(q):
        raise ValueError("q no es un número primo.")

    phi = (p - 1) * (q - 1)

    if e <= 1:
        raise ValueError("El exponente e es menor o igual a 1 y debería ser mayor a 1.")

    if mcd_euclides(e, phi) != 1:
        raise ValueError("El exponente e no es primo relativo con phi.")

    return p, q, e, n, phi

def validar_mensaje(mensaje):
    if mensaje == "":
        raise ValueError("Debe escribir un mensaje, no puede estar vacío.")

    for i in range(len(mensaje)):
        caracter = mensaje[i]
        codigo_caracter = ord(caracter)
        
        if codigo_caracter < 32 or codigo_caracter > 126:
            raise ValueError(f"El mensaje solo puede tener códigos de 32 a 126. El carácter erróneo tiene codigo: {codigo_caracter}, se encuentra en la posición {i + 1}.")

def validar_cifrado(texto_c, n):
    if texto_c == "":
        raise ValueError("Debe escribir el mensaje cifrado C.")
   
    partes = texto_c.split(" ")
    lista_bloques = []

    for i in range(len(partes)):
        parte = partes[i]
        num_bloque = i + 1

        if len(parte) != 6:
            raise ValueError(f"El bloque {num_bloque} de C debe tener exactamente 6 digitos y los bloques se separan con un solo espacio.")
        
        for caracter in parte:
            if caracter not in "0123456789":
                raise ValueError(f"El bloque {num_bloque} de C debe tener solo digitos del 0 al 9.")
            
        valor = int(parte)

        if valor >= n:
            raise ValueError(f"El bloque {num_bloque} de C debe ser menor que n.")

        lista_bloques.append(valor)

    return lista_bloques

def validar_longitud(texto_l, cantidad_bloques):
    k = cantidad_bloques
    par = 2 * k
    impar = 2 * k - 1
    
    longitud = leer_entero(texto_l, "L")

    if longitud != par and longitud != impar:
        raise ValueError(f"La longitud solo acepta {impar} o {par} y L debe corresponder a la cantidad de bloques: {k}.")

    return longitud

def validar_codigos(codigo1, codigo2, numero_bloque):
    if codigo1 < 32 or codigo1 > 126 or codigo2 < 32 or codigo2 > 126:
        raise ValueError(f"El bloque {numero_bloque} da los códigos {codigo1} y {codigo2}, que no se encuentran entre 32 y 126. Revisar p, q y e  sean los mismos con los que se encriptó y que C esté completo.")

def validar_relleno(texto, longitud):
    if longitud % 2 != 0 and texto[-1] != " ":
        raise ValueError("Como L es impar, el último carácter recuperado debería ser el espacio de relleno. Revisar que L, p, q, e y C sean los mismos con los que se encriptó.")