from rsa_app.interfaz.ventana import Ventana


def escribir(campo, texto):
    campo.delete(0, "end")
    campo.insert(0, texto)


def leer_resumen(pestana):
    return pestana.resumen.get("1.0", "end-1c")


def leer_tabla(pestana):
    filas = []
    for elemento in pestana.tabla.tabla.get_children():
        filas.append(list(pestana.tabla.tabla.item(elemento, "values")))
    return filas


ventana = Ventana()
ventana.update()
assert ventana.title() == "Criptografía RSA"

encriptar = ventana.marco_encriptar.winfo_children()[0]
desencriptar = ventana.marco_desencriptar.winfo_children()[0]
assert ventana.marco_encriptar.winfo_ismapped()
assert not ventana.marco_desencriptar.winfo_ismapped()
assert ventana.boton_encriptar.cget("fg_color") == "black"

escribir(encriptar.campo_mensaje, "RSA")
escribir(encriptar.campo_p, "367")
escribir(encriptar.campo_q, "373")
escribir(encriptar.campo_e, "17")
encriptar.ejecutar()
ventana.update()

resumen = leer_resumen(encriptar)
for texto in ['"RSA" (3 caracteres)', "Longitud L: 3", '"RSA "', "n = 136891", "φ = 136152", "MCD(e, φ) = 1", "(17, 136891)"]:
    assert texto in resumen, texto
assert encriptar.campo_c.get() == "026054 123875"
assert encriptar.etiqueta_error.cget("text") == ""
assert leer_tabla(encriptar) == [["1", '"RS"', "082 083", "082083", "026054"], ["2", '"A "', "065 032", "065032", "123875"]]

cifrado = encriptar.campo_c.get()
ventana.mostrar_desencriptar()
ventana.update()
assert ventana.marco_desencriptar.winfo_ismapped()
assert not ventana.marco_encriptar.winfo_ismapped()
assert ventana.boton_desencriptar.cget("fg_color") == "black"

escribir(desencriptar.campo_c, cifrado)
escribir(desencriptar.campo_l, "3")
escribir(desencriptar.campo_p, "367")
escribir(desencriptar.campo_q, "373")
escribir(desencriptar.campo_e, "17")
desencriptar.ejecutar()
ventana.update()

resumen = leer_resumen(desencriptar)
for texto in ['Mensaje recuperado: "RSA" (3 caracteres)', "Longitud L: 3", '"RSA "', "d = 8009", "(8009, 136891)"]:
    assert texto in resumen, texto
assert desencriptar.etiqueta_error.cget("text") == ""
assert leer_tabla(desencriptar) == [["1", "026054", "082083", "082 083", '"RS"'], ["2", "123875", "065032", "065 032", '"A "']]

escribir(desencriptar.campo_l, "6")
desencriptar.ejecutar()
ventana.update()
assert desencriptar.etiqueta_error.cget("text") != ""
assert leer_resumen(desencriptar) == ""
assert leer_tabla(desencriptar) == []

escribir(desencriptar.campo_l, "3")
desencriptar.ejecutar()
ventana.update()
assert desencriptar.etiqueta_error.cget("text") == ""
assert '"RSA" (3 caracteres)' in leer_resumen(desencriptar)

desencriptar.limpiar()
ventana.update()
for campo in [desencriptar.campo_c, desencriptar.campo_l, desencriptar.campo_p, desencriptar.campo_q, desencriptar.campo_e]:
    assert campo.get() == ""
assert leer_resumen(desencriptar) == ""
assert leer_tabla(desencriptar) == []

ventana.mostrar_encriptar()
mensajes = ["  RSA  ", "a  b   c", "Abc 123 #$%!", " I", "~"]
todos = ""
for codigo in range(32, 127):
    todos = todos + chr(codigo)
mensajes.append(todos)
for mensaje in mensajes:
    escribir(encriptar.campo_mensaje, mensaje)
    encriptar.ejecutar()
    ventana.update()
    assert encriptar.campo_mensaje.get() == mensaje
    assert len(leer_tabla(encriptar)) == (len(mensaje) + 1) // 2
    escribir(desencriptar.campo_c, encriptar.campo_c.get())
    escribir(desencriptar.campo_l, str(len(mensaje)))
    escribir(desencriptar.campo_p, "367")
    escribir(desencriptar.campo_q, "373")
    escribir(desencriptar.campo_e, "17")
    desencriptar.ejecutar()
    ventana.update()
    assert "Mensaje recuperado: " + '"' + mensaje + '"' in leer_resumen(desencriptar), mensaje
    assert leer_tabla(desencriptar)[0][4] == '"' + (mensaje + " ")[0:2] + '"', mensaje

escribir(encriptar.campo_mensaje, " I")
encriptar.ejecutar()
ventana.update()
assert encriptar.campo_c.get() == "000207"

escribir(encriptar.campo_mensaje, "Señor")
encriptar.ejecutar()
ventana.update()
assert "241" in encriptar.etiqueta_error.cget("text")
assert leer_resumen(encriptar) == ""
assert encriptar.campo_c.get() == ""
assert leer_tabla(encriptar) == []

escribir(encriptar.campo_mensaje, "RSA")
escribir(encriptar.campo_p, "361")
encriptar.ejecutar()
ventana.update()
assert encriptar.etiqueta_error.cget("text") != ""
assert encriptar.campo_c.get() == ""

encriptar.limpiar()
ventana.update()
for campo in [encriptar.campo_mensaje, encriptar.campo_p, encriptar.campo_q, encriptar.campo_e]:
    assert campo.get() == ""
assert encriptar.etiqueta_error.cget("text") == ""

ventana.destroy()
print("Pruebas de la interfaz superadas.")
