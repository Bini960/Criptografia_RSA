import random
import unittest

from rsa_app.matematica import (
    bezout_matricial,
    es_primo,
    exponenciacion_modular,
    factorizacion_prima,
    inverso_modular,
    mcd_euclides,
)

ENTRADAS_NO_ENTERAS = [2.5, "3", True]


def primos_por_criba(limite: int) -> set[int]:
    marcado = [True] * limite
    marcado[0] = marcado[1] = False
    for i in range(2, limite):
        if marcado[i] and i * i < limite:
            for multiplo in range(i * i, limite, i):
                marcado[multiplo] = False
    return {i for i in range(limite) if marcado[i]}


def potencia_paso_a_paso(b: int, e: int, n: int) -> int:
    resultado = 1
    for _ in range(e):
        resultado = (resultado * b) % n
    return resultado


class PruebaFactorizacionYPrimalidad(unittest.TestCase):
    def test_factorizaciones_conocidas(self):
        self.assertEqual(factorizacion_prima(360), [(2, 3), (3, 2), (5, 1)])
        self.assertEqual(factorizacion_prima(17), [(17, 1)])
        self.assertEqual(factorizacion_prima(136891), [(367, 1), (373, 1)])
        self.assertEqual(factorizacion_prima(1), [])

    def test_primos_del_proyecto(self):
        for n in [2, 3, 5, 367, 373, 42043, 63067, 499979]:
            with self.subTest(n=n):
                self.assertTrue(es_primo(n))

    def test_no_primos(self):
        for n in [-7, 0, 1, 4, 9, 341, 361, 126126, 136891]:
            with self.subTest(n=n):
                self.assertFalse(es_primo(n))

    def test_coincide_con_la_criba(self):
        limite = 20_000
        primos = primos_por_criba(limite)
        for n in range(limite):
            self.assertEqual(es_primo(n), n in primos, n)


class PruebaMcd(unittest.TestCase):
    def test_valores_conocidos(self):
        casos = [((43, 19), 1), ((662, 441), 1), ((48, 12), 12), ((12, 48), 12),
                 ((252, 198), 18), ((48, 48), 48), ((136152, 17), 1), ((136152, 3), 3)]
        for (a, b), esperado in casos:
            with self.subTest(a=a, b=b):
                self.assertEqual(mcd_euclides(a, b), esperado)

    def test_divide_a_ambos(self):
        rng = random.Random(2026)
        for _ in range(300):
            a, b = rng.randint(1, 10**12), rng.randint(1, 10**12)
            d = mcd_euclides(a, b)
            self.assertEqual((a % d, b % d), (0, 0))

    def test_entradas_invalidas(self):
        for invalido in [0, -1]:
            with self.assertRaises(ValueError):
                mcd_euclides(invalido, 6)
        for invalido in ENTRADAS_NO_ENTERAS:
            with self.assertRaises(TypeError):
                mcd_euclides(10, invalido)


class PruebaBezoutEInverso(unittest.TestCase):
    def test_coeficientes_conocidos(self):
        self.assertEqual(bezout_matricial(43, 19), (4, -9))
        self.assertEqual(bezout_matricial(17, 136152), (8009, -1))

    def test_identidad_de_bezout(self):
        rng = random.Random(2026)
        pares = [(1, 1), (1, 29), (29, 1), (36, 12), (12, 36), (136153, 136152)]
        pares += [(rng.randint(1, 10**12), rng.randint(1, 10**12)) for _ in range(300)]
        for a, b in pares:
            x, y = bezout_matricial(a, b)
            self.assertEqual(a * x + b * y, mcd_euclides(a, b), (a, b))

    def test_inversos_conocidos(self):
        casos = [((17, 136152), 8009),
                 ((7, 11), 8),
                 ((39, 58), 3),
                 ((13, 3220), 2477),
                 ((680777, 136152), 8009),
                 ((136153, 136152), 1)]
        for (a, m), esperado in casos:
            with self.subTest(a=a, m=m):
                self.assertEqual(inverso_modular(a, m), esperado)

    def test_inverso_en_rango_y_correcto(self):
        rng = random.Random(7)
        for _ in range(300):
            m = rng.randint(2, 10**6)
            a = rng.randint(1, 10**7)
            if mcd_euclides(a, m) != 1:
                continue
            d = inverso_modular(a, m)
            self.assertTrue(1 <= d < m)
            self.assertEqual((a * d) % m, 1 % m)

    def test_sin_inverso(self):
        for a, m in [(2, 136152), (3, 136152), (6, 9)]:
            with self.assertRaises(ValueError):
                inverso_modular(a, m)
        with self.assertRaises(ValueError):
            inverso_modular(5, 1)


class PruebaExponenciacion(unittest.TestCase):
    def test_valores_conocidos(self):
        casos = [((82083, 17, 136891), 26054),
                 ((65032, 17, 136891), 123875),
                 ((26054, 8009, 136891), 82083),
                 ((123875, 8009, 136891), 65032),
                 ((7, 24, 11), 3),
                 ((79, 79, 100), 19),
                 ((1234, 13, 3337), 2779),
                 ((2779, 2477, 3337), 1234),
                 ((7, 14, 47), 34)]
        for (b, e, n), esperado in casos:
            with self.subTest(b=b, e=e, n=n):
                self.assertEqual(exponenciacion_modular(b, e, n), esperado)

    def test_coincide_con_la_version_paso_a_paso(self):
        rng = random.Random(11)
        for _ in range(300):
            b, e, n = rng.randint(0, 10**6), rng.randint(1, 400), rng.randint(2, 10**6)
            self.assertEqual(exponenciacion_modular(b, e, n), potencia_paso_a_paso(b, e, n))

    def test_base_cero(self):
        self.assertEqual(exponenciacion_modular(0, 8009, 136891), 0)

    def test_exponente_de_4300_digitos(self):
        p = 1_000_000_007
        e = 10**4290 * (p - 1) + 1
        self.assertEqual(len(str(e)), 4300)
        self.assertEqual(exponenciacion_modular(123456789, e, p), 123456789)

    def test_exponente_enorme_en_rsa(self):
        e = 17 + 10**4290 * 136152
        self.assertEqual(exponenciacion_modular(82083, e, 136891), 26054)

    def test_entradas_invalidas(self):
        with self.assertRaises(ValueError):
            exponenciacion_modular(-1, 13, 11)
        for e in [0, -1]:
            with self.assertRaises(ValueError):
                exponenciacion_modular(7, e, 11)
        with self.assertRaises(ValueError):
            exponenciacion_modular(7, 13, 1)
        for posicion in range(3):
            for invalido in ENTRADAS_NO_ENTERAS:
                argumentos = [7, 13, 11]
                argumentos[posicion] = invalido
                with self.assertRaises(TypeError):
                    exponenciacion_modular(*argumentos)


if __name__ == "__main__":
    unittest.main()
