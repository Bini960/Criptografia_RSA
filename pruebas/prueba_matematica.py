from rsa_app.matematica import bezout_matricial, es_primo, exponenciacion_modular, inverso_modular, mcd_euclides


def primo_por_division(n):
    if n < 2:
        return False
    for d in range(2, n):
        if n % d == 0:
            return False
    return True


def potencia_paso_a_paso(b, e, n):
    resultado = 1
    for i in range(e):
        resultado = (resultado * b) % n
    return resultado


for n in [2, 3, 5, 367, 373, 42043, 63067, 499979]:
    assert es_primo(n), n
for n in [0, 1, 4, 9, 341, 361, 126126, 136891]:
    assert not es_primo(n), n
for n in range(2000):
    assert es_primo(n) == primo_por_division(n), n

assert mcd_euclides(48, 12) == 12
assert mcd_euclides(12, 48) == 12
assert mcd_euclides(662, 441) == 1
assert mcd_euclides(43, 19) == 1
assert mcd_euclides(136152, 17) == 1
assert mcd_euclides(136152, 9) == 9

for a, b in [(43, 19), (17, 136152), (1, 29), (36, 12), (12, 36), (136153, 136152)]:
    x, y = bezout_matricial(a, b)
    assert a * x + b * y == mcd_euclides(a, b), (a, b)
assert bezout_matricial(43, 19) == (4, -9)

assert inverso_modular(7, 11) == 8
assert inverso_modular(39, 58) == 3
assert inverso_modular(13, 3220) == 2477
assert inverso_modular(17, 136152) == 8009
assert inverso_modular(680777, 136152) == 8009
assert inverso_modular(136153, 136152) == 1
try:
    inverso_modular(2, 136152)
except Exception:
    pass
else:
    raise AssertionError("2 no tiene inverso módulo 136152.")

assert exponenciacion_modular(7, 24, 11) == 3
assert exponenciacion_modular(79, 79, 100) == 19
assert exponenciacion_modular(7, 14, 47) == 34
assert exponenciacion_modular(1234, 13, 3337) == 2779
assert exponenciacion_modular(2779, 2477, 3337) == 1234
assert exponenciacion_modular(82083, 17, 136891) == 26054
assert exponenciacion_modular(65032, 17, 136891) == 123875
assert exponenciacion_modular(26054, 8009, 136891) == 82083
for b in range(1, 60):
    for e in range(1, 60):
        assert exponenciacion_modular(b, e, 47) == potencia_paso_a_paso(b, e, 47), (b, e)

print("Pruebas de matematica.py superadas.")
