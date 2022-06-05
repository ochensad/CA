from numpy.polynomial.legendre import leggauss
from numpy import arange
from math import sqrt
import matplotlib.pyplot as plt
from math import pi, cos, sin, exp


# умножает полиномы, заданные в виде коэффициентов, т.е. x^2 - 1 === [-1, 0, 1]
def mul_polynomes(src, mult):
    dst = []
    for i in range(len(src) + len(mult) - 1):
        dst.append(0)
    for i in range (len(src)):
        for j in range (len(mult)):
            dst[i + j] += src[i] * mult[j]
    return dst
# вычисляет производную полинома
def derivative(pol):
    dst = []
    for i in range(1, len(pol)):
        dst.append(pol[i] * i)
    return dst
# находит полином Лежандра Pn по определению
def find_leg(n):
    st = 1
    fact = 1
    pol = [1]
    mult = [-1, 0, 1]
    
    for i in range (1, n + 1):
        st *= 2
        fact *= i
        pol = mul_polynomes(pol, mult)
        
    for i in range(n):
        pol = derivative(pol)
        
    for i in range(len(pol)):
        pol[i] *= 1 / (st * fact)
    return pol
# Вычисляет значение полинома
def get_pol_value(pol, arg):
    val = 0
    for i in range(len(pol)):
        val += pol[i] * (arg ** i)
    return val
# метод половинного деления (полином, отриц. конец отрезка, полжит. конец отрезка),
# работает корректно только тогда, когда на концах отрезка значения  функции разного знака
def half_division_method(pol, left, right, grad):
    mid = (left + right) / 2
    if abs(left - right) < 1e-5:
        return mid
    test = get_pol_value(pol, mid)
    if grad:
        if test > 0:
            return half_division_method(pol, left, mid, grad)
        elif test < 0:
            return half_division_method(pol, mid, right, grad)
    else:
        if test < 0:
            return half_division_method(pol, left, mid, grad)
        elif test > 0:
            return half_division_method(pol, mid, right, grad)
    return mid
# находит все отрезки, на которых есть корни, и вычисляет корни
# с помощью метода половинного деления
def find_roots(pol):
    n = len(pol) - 1
    k = 0
    if get_pol_value(pol, -1) * get_pol_value(pol, 0) > 0:
        k = 0
    else:
        k = 1
    segments = [[-1, 0]]
    t = n - n / 2
    while (k < t):
        seg_tmp = []
        k = 0
        for i in range(len(segments)):
            mid = (segments[i][1] + segments[i][0]) / 2
            seg_tmp.append( [segments[i][0], mid] )
            seg_tmp.append( [mid, segments[i][1]] )
            if get_pol_value(pol, mid) == 0:
                k += 1
            else:
                if get_pol_value(pol, segments[i][0]) * get_pol_value(pol, mid) <= 0:
                    k += 1
                if get_pol_value(pol, segments[i][1]) * get_pol_value(pol, mid) <= 0:
                    k += 1     
        segments = seg_tmp
    roots = []
    for seg in segments:
        left = get_pol_value(pol, seg[0])
        right = get_pol_value(pol, seg[1])
        if left == 0:
            roots.append(seg[0])
        if right == 0:
            continue
        if get_pol_value(pol, seg[0]) < 0 and get_pol_value(pol, seg[1]) > 0:
            roots.append(half_division_method(pol, seg[0], seg[1], True))
        if get_pol_value(pol, seg[0]) > 0 and get_pol_value(pol, seg[1]) < 0:
            roots.append(half_division_method(pol, seg[0], seg[1], False))
    if get_pol_value(pol, segments[len(segments) - 1][1]) == 0:
        roots.append(segments[len(segments) - 1][1])
    t = int(n / 2)
    for i in range (t):
        roots.append(-roots[i])
    return roots
# решение СЛАУ с помощью метода Гаусса 
def solve_slau_Gauss(matrix, n):
    for k in range(n):
        for i in range(k + 1, n):
            coeff = -(matrix[i][k] / matrix[k][k])
            for j in range(k, n + 1):
                matrix[i][j] += coeff * matrix[k][j]

    a = [0 for i in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(n - 1, i, -1):
            matrix[i][n] -= a[j] * matrix[i][j]
        a[i] = matrix[i][n] / matrix[i][i]
    return a
# находит коэффициенты в основной системе (узлы найдены с помощью полиномов Лежандра)
def find_coefs(nodes):
    matrix = []
    for i in range(len(nodes)):
        array = []
        for j in range(len(nodes)):
            array.append(nodes[j] ** i)
        if i % 2 == 0:
            array.append(2 / (i + 1))
        else:
            array.append(0)
        matrix.append(array)
    res = solve_slau_Gauss(matrix, len(nodes))
    return res

def main_func():
    func = lambda x, y: sqrt(x ** 2 + y ** 2)
    return func


def F2_1(F2, val):
    return lambda x: F2(val, x)

def simpson(F, a, b, num):
    h = (b - a) / (num - 1)
    x = a
    res = 0

    for i in range((num - 1) // 2):
        res += F(x) + 4 * F(x + h) + F(x + 2 * h)
        x += 2 * h
    
    return res * (h / 3)

def t_x(t, a, b):
    return (b + a) / 2 + (b - a) * t / 2

def map(a, b, x, c, d):
    # t = (x - a) / (b - a)
    # t = t - 0.5
    # t = t * pi
    # t = cos(t)
    # t = 1
    return [-sqrt(x * (2 - x)), sqrt(x * ( 2 - x))] 

def gauss(F, a, b, num):
    leg = find_leg(num)
    args = find_roots(leg)
    coeffs = find_coefs(args)
    res = 0
    for i in range(num):
        res += (b - a) / 2 * coeffs[i] * F(t_x(args[i], a, b))
    return res


def integr_2(F, limit, num, integr):
    first = lambda x: integr[1](F2_1(F, x), map(limit[0][0], limit[0][1], x, limit[1][0], limit[1][1])[0], 
                                map(limit[0][0], limit[0][1], x, limit[1][0], limit[1][1])[1], num[1])
    # first = lambda x: integr[1](F2_1(F, x), limit[1][0], 
    #                             limit[1][1], num[1])
    res = integr[0](first, limit[0][0], limit[0][1], num[0])
    return res

def main():
    n = int(input("Input N (integer): "))
    m = int(input("Input M (integer): "))
    flag = bool(int(input("Выберете первый метод (0 - Симпсон, 1 - Гаусс): ")))
    F1 = gauss if flag else simpson
    flag = bool(int(input("Выберете второй метод (0 - Симпсон, 1 - Гаусс): ")))
    F2 = gauss if flag else simpson

    res = integr_2(main_func(), [[0, 2], [-1, 1]], [n, m], [F1, F2])
    print(res)

main()