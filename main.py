import sys

try:
    from rsa_app.interfaz.ventana import VentanaPrincipal
except ModuleNotFoundError as error:
    if error.name == "customtkinter":
        print("Falta la biblioteca CustomTkinter.")
        print("Instálala con: python -m pip install -r requirements.txt")
        sys.exit(1)
    raise


def main() -> None:
    ventana = VentanaPrincipal()
    ventana.mainloop()


if __name__ == "__main__":
    main()
