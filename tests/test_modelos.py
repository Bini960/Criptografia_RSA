import dataclasses
import unittest

from rsa_app.modelos import (
    ErrorValidacion,
    FilaBloque,
    ParametrosRSA,
    ResultadoDesencriptacion,
    ResultadoEncriptacion,
)


class PruebaModelos(unittest.TestCase):
    def setUp(self):
        self.parametros = ParametrosRSA(p=367, q=373, e=17, n=136891, phi=136152, mcd_e_phi=1)
        self.filas = (
            FilaBloque(numero=1, pareja="RS", codigos=(82, 83), bloque_m=82083, bloque_c=26054),
            FilaBloque(numero=2, pareja="A ", codigos=(65, 32), bloque_m=65032, bloque_c=123875),
        )

    def encriptacion(self, mensaje, longitud, tiene_relleno):
        return ResultadoEncriptacion(
            parametros=self.parametros, mensaje=mensaje, longitud=longitud,
            tiene_relleno=tiene_relleno, filas=self.filas, cifrado="026054 123875",
        )

    def test_error_validacion_es_value_error(self):
        self.assertTrue(issubclass(ErrorValidacion, ValueError))

    def test_llave_publica_y_mensaje_con_relleno(self):
        resultado = self.encriptacion("RSA", 3, True)
        self.assertEqual(resultado.llave_publica, (17, 136891))
        self.assertEqual(resultado.mensaje_con_relleno, "RSA ")

    def test_mensaje_sin_relleno(self):
        resultado = self.encriptacion("HOLA", 4, False)
        self.assertEqual(resultado.mensaje_con_relleno, "HOLA")

    def test_llave_privada(self):
        resultado = ResultadoDesencriptacion(
            parametros=self.parametros, d=8009, longitud=3, tiene_relleno=True,
            filas=self.filas, texto_recuperado="RSA ", mensaje="RSA",
        )
        self.assertEqual(resultado.llave_privada, (8009, 136891))

    def test_resultados_no_se_pueden_modificar(self):
        with self.assertRaises(dataclasses.FrozenInstanceError):
            self.parametros.n = 1
        with self.assertRaises(dataclasses.FrozenInstanceError):
            self.encriptacion("RSA", 3, True).longitud = 4


if __name__ == "__main__":
    unittest.main()
