from typing import List, Callable as func
from numpy import linspace, array
from numpy.linalg import solve
from math import cos, pi, sqrt

# полином Лежандра
def leg_polym(n, x):
    if n < 2:
        return [1, x][n]

    P1 = leg_polym(n - 1, x)
    P2 = leg_polym(n - 2, x)

    return ((2 * n - 1) * x * P1 - (n - 1) * P2) / n


# производная полинома Лежандра
def leg_polym_deriv(n, x):
    P1 = leg_polym(n - 1, x)
    P2 = leg_polym(n, x)

    return n / (1 - x * x) * (P1 - x * P2)


# поиск корней с помощью метода Ньютона
def leg_roots(n: int, eps: float = 1e-12) -> List[float]:
    roots = [cos(pi * (4 * i + 3) / (4 * n + 2)) for i in range(n)]  # нач. приближение

    for i, root in enumerate(roots):
        root_val = leg_polym(n, root)

        while abs(root_val) > eps:
            root -= root_val / leg_polym_deriv(n, root)
            root_val = leg_polym(n, root)

        roots[i] = root

    return roots


# интегрирование от -1 до 1
def norm_gauss_integ(f, n):
    t = leg_roots(n)  # корни полинома Лежандра n-ой степени
    T = array([[t_i**k for t_i in t] for k in range(n)])

    int_tk = lambda k: 2 / (k + 1) if k % 2 == 0 else 0
    b = array([int_tk(k) for k in range(n)])  # правая часть

    A = solve(T, b)  # находим коэффициенты А

    return sum(A_i * f(t_i) for A_i, t_i in zip(A, t))


# перенос интегрирования [-1, 1] на [a, b]
def gauss_integ(f, a, b, n):
    mean, diff = (a + b) / 2, (b - a) / 2
    g = lambda t: f(mean + diff * t)
    return diff * norm_gauss_integ(g, n)


# интегрирование по формуле Симпсона
def simp_integ(f, a, b, n):
    h = (b - a) / (n - 1)
    x = a
    res = 0

    for i in range((n - 1) // 2):
        res += f(x) + 4 * f(x + h) + f(x + 2 * h)
        x += 2 * h

    return res * (h / 3)


# композиция методов интегрирования
# сначала для фиксированного у 1ым методом вычисляется итеграл
# далее идёт интегрирование по игрекам 2ым методом
def compose_integ(f, a1, b1, a2, b2, method_1, method_2, n1, n2):
    F = lambda x: method_1(lambda y: f(x, y), a2, b2, n1)
    return method_2(F, a1, b1, n2)


def function_integ(f, a, b, c, d, n, m):
    return compose_integ(f, a, b, c, d, gauss_integ, simp_integ, n, m)


def in_circle(x, y):
    return (x**2 + y**2) - 2 * x <= 0
    # return True


# функция получения интеграла
def function(n, m):
    f = lambda x, y: sqrt(x**2 + y**2) if in_circle(x, y) else 0  # основная функция
    return function_integ(f, 0, 2, -1, 1, n, m)


print(function(7, 1000))


def f1(x):
    return 4 * x**2


print(gauss_integ(f1, 4, 5, 7))
print(simp_integ(f1, 4, 5, 1000))
