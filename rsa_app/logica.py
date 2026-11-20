def es_primo(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False

    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


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


def inverso_modular(a, m):
    a_mod = a % m
    if a_mod == 0:
        raise Exception('No existe el inverso modular')

    x, y = bezout_matricial(a_mod, m)
    if (a_mod * x + m * y) != 1:
        raise Exception('No existe el inverso modular')

    return x % m


def exponenciacion_modular(b: int, e: int, n: int) -> int:
    if type(b) is not int or type(e) is not int or type(n) is not int:
        raise TypeError("La base, el exponente y el módulo deben ser enteros")
    if b <= 0 or e <= 0:
        raise ValueError("La base y el exponente deben ser enteros positivos")
    if n < 2:
        raise ValueError("El módulo debe ser mayor o igual a 2")

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
