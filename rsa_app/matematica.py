import sys

LIMITE_RECURSION = 20_000


def factorizacion_prima(n: int) -> list[tuple[int, int]]:
    factores = []
    d = 2

    while d * d <= n:
        if n % d == 0:
            potencia = 0
            while n % d == 0:
                potencia += 1
                n //= d
            factores.append((d, potencia))
        d += 1

    if n > 1:
        factores.append((n, 1))

    return factores


def es_primo(n: int) -> bool:
    return factorizacion_prima(n) == [(n, 1)]


def mcd_euclides(a: int, b: int) -> int:
    if type(a) is not int or type(b) is not int:
        raise TypeError("Las entradas a y b deben ser números enteros")
    if a <= 0 or b <= 0:
        raise ValueError("Las entradas a y b deben ser enteros positivos")

    while b != 0:
        a, b = b, a % b

    return a


def bezout_matricial(a: int, b: int) -> tuple[int, int]:
    if type(a) is not int or type(b) is not int:
        raise TypeError("Las entradas a y b deben ser números enteros")
    if a <= 0 or b <= 0:
        raise ValueError("Las entradas a y b deben ser enteros positivos")

    m11, m12 = 1, 0
    m21, m22 = 0, 1
    det = 1

    while a % b != 0:
        q = a // b
        r = a % b

        m11, m12 = m11 * q + m12, m11
        m21, m22 = m21 * q + m22, m21

        det = -det
        a, b = b, r

    x = -m21 * det
    y = m11 * det

    return (x, y)


def inverso_modular(a: int, m: int) -> int:
    if type(m) is int and m < 2:
        raise ValueError("El módulo debe ser mayor o igual a 2")
    divisor = mcd_euclides(a, m)
    if divisor != 1:
        raise ValueError(f"{a} no tiene inverso módulo {m}, porque MCD({a}, {m}) = {divisor}")

    x, _ = bezout_matricial(a, m)
    return x % m


def exponenciacion_modular(b: int, e: int, n: int) -> int:
    if type(b) is not int or type(e) is not int or type(n) is not int:
        raise TypeError("La base, el exponente y el módulo deben ser enteros")
    if b < 0:
        raise ValueError("La base no puede ser negativa")
    if e <= 0:
        raise ValueError("El exponente debe ser un entero positivo")
    if n < 2:
        raise ValueError("El módulo debe ser mayor o igual a 2")

    if sys.getrecursionlimit() < LIMITE_RECURSION:
        sys.setrecursionlimit(LIMITE_RECURSION)

    def mpower(base: int, exp: int, mod: int) -> int:
        if exp == 0:
            return 1

        mitad = mpower(base, exp // 2, mod)
        cuadrado_mod = (mitad * mitad) % mod

        if exp % 2 == 0:
            return cuadrado_mod
        else:
            return (base * cuadrado_mod) % mod

    return mpower(b, e, n)
