class coefficients:
    def __init__(self, x, y, a=None, b=None, c=None, d=None, h=None, f=None, e=None, n=None) -> None:
        self.x = x
        self.y = y
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.h = h
        self.f = f
        self.e = e
        self.n = n

    def h_calc(self, prev_str=None):
        if prev_str:
            self.h = self.x - prev_str.x

    def E_calc(self, prev=None, prev_prev=None):
        if prev_prev:
            self.e = -(prev.h / (prev_prev.h * prev.e + 2 * (prev_prev.h + prev.h)))

    def f_calc(self, prev=None, prev_prev=None):
        if prev and prev_prev:
            self.f = 3 * ((self.y - prev.y) / self.h - (prev.y - prev_prev.y) / prev.h)

    def n_calc(self, prev=None, prev_prev=None):
        if prev_prev:
            self.n = (prev.f - prev_prev.h * prev.n) \
                     / (prev_prev.h * prev.e + 2 * (prev_prev.h + prev.h))

    def c_calc(self, prev=None, next=None):
        if prev and next:
            self.c = -self.h * next.c / (prev.h * self.e + 2 * (prev.h + self.h)) + \
                     (self.f - prev.h * self.n) / (prev.h * self.e + 2 * (prev.h + self.h))

    def a_calc(self, prev=None):
        if prev:
            self.a = prev.y

    def b_calc(self, prev=None, next=None):
        if prev and next:
            self.b = (self.y - prev.y) / self.h - self.h * (next.c + 2 * self.c) / 3

    def d_calc(self, next=None):
        if next:
            self.d = (next.c - self.c) / (3 * self.h)

class point:
    def __init__(self, x, y) -> None:
        if type(x) == list:
            buf = x
            self.x = buf[0]
            self.y = buf[1]
        else:
            self.x = x
            self.y = y

def read_points_from_file(filename:str) -> list:
    dots = []
    with open(filename) as f:
        line = f.readline()
        while line:
            line = line.strip('\n')
            dots.append(point(list(map(float, line.split())), 0))
            line = f.readline()
    dots.sort(key=lambda p: p.x, reverse=False)
    return dots

def find_start_and_stop(n, x, dots):
    if n + 1 > len(dots):
        print('Недостаточно точек для заданного n!')
        exit(1)

    index = 0
    for dot in dots:
        if dot.x < x:
            index += 1

    half1 = (n + 1) // 2
    half2 = (n + 1) - half1

    start_ind = (index - half1) if (index - half1 >= 0) else 0
    stop_ind = (index + half2) if (index + half2 <= len(dots)) else len(dots)

    if start_ind == 0:
        stop_ind += abs(index - half1)

    if stop_ind == len(dots):
        start_ind -= index + half2 - len(dots)

    return start_ind, stop_ind

def culc_func_for_newton(args, dictt):
    if len(args) == 1:
        return dictt[args[0]]
    if len(args) == 2:
        res = (dictt[args[0]] - dictt[args[1]]) / (args[0] - args[1])
        return res
    else:
        return (culc_func_for_newton(args[:-1], dictt) - culc_func_for_newton(args[1:], dictt)) / (args[0] - args[-1])

def newton(n, x, dots):
    si, ei = find_start_and_stop(n, x, dots)

    res = 0
    fd = {}
    for i in range(si, ei):
        fd[dots[i].x] = dots[i].y
    
    for i in range(si, ei): 
        j = i - si + 1
        arg = []
        loc_sum = 1
        for m in range(j):
            arg.append(dots[si + m].x)
        
        if j == 3:
            loc_sum *= culc_func_for_newton(arg, fd) * 2
            res += loc_sum

        if j == 4:
            loc_sum *= culc_func_for_newton(arg, fd) * (6 * x - 2 * (dots[si].x + dots[si + 1].x + dots[si + 2].x))
            res += loc_sum
        
    return res / 2

def newton2(n, x, dots):
    start_ind, stop_ind = find_start_and_stop(n, x, dots)

    res = 0
    func_dict = {}
    for i in range(start_ind, stop_ind):
        func_dict[dots[i].x] = dots[i].y

    for i in range(start_ind, stop_ind):
        j = i - start_ind + 1
        args = []
        loc_sum = 1
        for k in range(j):
            args.append(dots[start_ind + k].x)
            if k >= 1:
                loc_sum *= (x - dots[start_ind + k - 1].x)
        loc_sum *= culc_func_for_newton(args, func_dict)
        res += loc_sum

    return res

def fill_table(points:list, method:int, n:int):
    table = []
    for point in points:
        table.append(coefficients(point.x, point.y))

    for i in range(1, len(table)):
        table[i].h_calc(table[i - 1])

    for i in range(2, len(table)):
        table[i].f_calc(table[i - 1], table[i - 2])

    if method == 1:
        table[2].e = table[2].n = table[1].c = 0
        obj = coefficients(0, 0, c=0)
    elif method == 2:
        table[2].e = 0
        table[2].n = newton(n, points[0].x, points)
        table[1].c = newton(n, points[0].x, points)
        obj = coefficients(0, 0, c=0)
    elif method == 3:
        table[2].e = table[2].n = 0
        table[2].n = newton(n, points[0].x, points)
        table[1].c = newton(n, points[0].x, points)
        obj = coefficients(0, 0, c=newton(n, points[-1].x, points))

    for i in range(3, len(table)):
        table[i].E_calc(table[i - 1], table[i - 2])
        table[i].n_calc(table[i - 1], table[i - 2])
            
    for i in range(len(table) - 1, 1, -1):
        if i == len(table) - 1:
                table[i].c_calc(table[i - 1], obj)
        else:
            table[i].c_calc(table[i - 1], table[i + 1])

    for i in range(1, len(table)):
        table[i].a_calc(table[i - 1])
    
    for i in range(len(table) - 1, 0, -1):
        if i == len(table) - 1:
                table[i].b_calc(table[i - 1], obj)
        else:
            table[i].b_calc(table[i - 1], table[i + 1])

    for i in range(len(table) - 1, 0, -1):
        if i == len(table) - 1:
                table[i].d_calc(obj)
        else:
            table[i].d_calc(table[i + 1])

    return table

def print_table(table):
    print("\n\n {:^85s}".format("Таблица коэффициентов"))
    print(" " + "-"*85)
    print("| {:^3s} | {:^7s} | {:^7s} | {:^7s} | {:^7s} | {:^7s} | {:^7s} | {:^7s} | {:^7s} |".format('№', 'a', 'b', 'c', 'd', 'h', 'f', 'e', 'n'))
    for i in range(1, len(table)):
        a = table[i]
        print("| {:^3d} | {:^7.4f} | {:^7.4f} | {:^7.4f} | {:^7.4f} | {:^7.4f} |".format(i, a.a, a.b, a.c, a.d, a.h), end='')
        if (a.h != None):
            print(" {:^7.4f} |".format(a.h), end='')
        else:
            print(" {:^7s} |".format('-'), end='')
        if (a.e != None):
            print(" {:^7.4f} |".format(a.e), end='')
        else:
            print(" {:^7s} |".format('-'), end='')
        if (a.n != None):
            print(" {:^7.4f} |".format(a.n), end='')
        else:
            print(" {:^7s} |".format('-'), end='')
        print()

    print(" " + "-"*85 + "\n")

def spline(x, p, method=1):
    if (len(p) <= 3):
        n = 2
    else:
        n = 3
    table = fill_table(p, method, n)
    index = 0
    for i in range(len(table)):
        if (table[i].x <= x):
            index += 1
    
    print_table(table)

    if index == 0 or index >= len(p):
        print(x, index, len(p))
        print('Невозможно посчитать значение!')
        return
    
    px = table[index - 1].x
    res = table[index].a + table[index].b * (x - px) + table[index].c * ((x - px) ** 2) \
        + table[index].d * ((x - px) ** 3)
    
    return res

def main():
    filename = input("Введите название файла: ")
    x = float(input("Введите значение х: "))
    points = read_points_from_file(filename)

    print("Варианты условий на границах:")
    print("1:", spline(x, points, 1))
    print("2:", spline(x, points, 2))
    print("3:", spline(x, points, 3))

    mx = (points[-1].x + points[0].x) / 2
    fx = points[0].x + 1e-5
    lx = points[-1].x -1e-5

    if (len(points) <= 3):
        n = 2
    else:
        n = 3
    print("Вариант сплайна 1")
    print('|{:^25s}| {:^12s} | {:^12s} |'.format('', 'Сплайн', 'Ньютон'))
    print('|  В середине х ={:8.5f} | {:12.9f} | {:12.9f} |'.format(round(mx), (spline(mx, points)), (newton2(n, mx, points))))
    print('|  Левый край х ={:8.5f} | {:12.9f} | {:12.9f} |'.format(round(fx), (spline(fx, points)), (newton2(n, fx, points))))
    print('| Правый край х ={:8.5f} | {:12.9f} | {:12.9f} |'.format(round(lx), (spline(lx, points)), (newton2(n, lx, points))))
    
    print("Вариант сплайна 2")
    print('|{:^25s}| {:^12s} | {:^12s} |'.format('', 'Сплайн', 'Ньютон'))
    print('|  В середине х ={:8.5f} | {:12.9f} | {:12.9f} |'.format(round(mx), (spline(mx, points, 2)), (newton2(n, mx, points))))
    print('|  Левый край х ={:8.5f} | {:12.9f} | {:12.9f} |'.format(round(fx), (spline(fx, points, 2)), (newton2(n, fx, points))))
    print('| Правый край х ={:8.5f} | {:12.9f} | {:12.9f} |'.format(round(lx), (spline(lx, points, 2)), (newton2(n, lx, points))))
    
    print("Вариант сплайна 3")
    print('|{:^25s}| {:^12s} | {:^12s} |'.format('', 'Сплайн', 'Ньютон'))
    print('|  В середине х ={:8.5f} | {:12.9f} | {:12.9f} |'.format(round(mx), (spline(mx, points, 3)), (newton2(n, mx, points))))
    print('|  Левый край х ={:8.5f} | {:12.9f} | {:12.9f} |'.format(round(fx), (spline(fx, points, 3)), (newton2(n, fx, points))))
    print('| Правый край х ={:8.5f} | {:12.9f} | {:12.9f} |'.format(round(lx), (spline(lx, points, 3)), (newton2(n, lx, points))))
    



if __name__ == "__main__":
    main()