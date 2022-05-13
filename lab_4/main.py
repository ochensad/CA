import random
import numpy as np
from matplotlib import pyplot as plt


def approximate_2d_y(table, n):
    a = [[sum(list(map(lambda row: row[1] ** (i + j) * row[2], table))) for j in range(n + 1)] for i in range(n + 1)]
    b = [sum(list(map(lambda row: row[1] ** i * row[0], table))) for i in range(n + 1)]
    c = list(np.linalg.solve(a, b))

    def approx_func(y):
        res = 0
        y_degree = 1
        for ci in c:
            res += y_degree * ci
            y_degree *= y
        return res

    return approx_func


def approximate_2d(table, n):
    a = [[sum(list(map(lambda row: row[0] ** (i + j) * row[2], table))) for j in range(n + 1)] for i in range(n + 1)]
    b = [sum(list(map(lambda row: row[0] ** i * row[1] * row[2], table))) for i in range(n + 1)]
    c = list(np.linalg.solve(a, b))
    print('Coeffs:', c)

    def approx_func(x):
        res = 0
        x_degree = 1
        for ci in c:
            res += x_degree * ci
            x_degree *= x
        return res

    return approx_func


def value(x, y, x_pow, y_pow, is_change_func):
    if is_change_func:
        return x ** x_pow * np.exp(y) ** y_pow
    return x ** x_pow * y ** y_pow


def approximate_3d(table, n, is_change_func):
    a = []
    b = []
    for i in range(n + 1):
        for j in range(n + 1 - i):
            a_row = []
            for k in range(n + 1):
                for t in range(n + 1 - k):
                    a_row.append(
                        sum(list(map(lambda row: value(row[0], row[1], k + i, t + j, is_change_func) * row[3], table))))
            a.append(a_row)
            b.append(sum(list(map(lambda row: value(row[0], row[1], i, j, is_change_func) * row[2] * row[3], table))))

    c = list(np.linalg.solve(a, b))

    print('Coeffs:', c)

    def approx_func(x, y):
        res = 0
        x_degree = 1
        c_index = 0
        x_pow = 0
        for i in range(n + 1):
            y_degree = 1
            y_pow = 0
            for j in range(n + 1 - i):
                res += c[c_index] * value(x, y, x_pow, y_pow, is_change_func)
                y_degree *= y
                y_pow += 1
                c_index += 1
            x_degree *= x
            x_pow += 1
        return res

    return approx_func


def print_2D_table(table):
    print("\n\t\tТаблица\n\n" +
          "  №    |     X     |     Y    |    W \n" + 40 * "-")

    size = len(table)

    for i in range(size):
        print("  %-3d  |   %-5.2f   |   %-4.2f   |   %-5.2f   "
              % (i + 1, table[i][0], table[i][1], table[i][2]))


def print_3D_table(table):
    print("\n\t\t\tТаблица\n\n" +
          "  №    |      X       |     Y       |       Z     |    W \n" + 59 * "-")

    size = len(table)

    for i in range(size):
        print("  %-3d  |   %-8.2f   |   %-7.2f   |   %-7.2f   |   %-8.2f   "
              % (i + 1, table[i][0], table[i][1], table[i][2], table[i][3]))


def main():
    x_range = [100, 150]
    y_range = [-0.3, 1]
    z_range = [-10, 10]
    w_range = [-15, 15]
    N = 5
    count_points = 100
    mode = "3d"
    n = 2
    is_random = False
    if is_random:
        if mode == "3d":
            table = [[random.random() * (x_range[1] - x_range[0]) + x_range[0],
                      random.random() * (y_range[1] - y_range[0]) + y_range[0],
                      random.random() * (z_range[1] - z_range[0]) + z_range[0],
                      random.random() * (w_range[1] - w_range[0]) + w_range[0]] for _ in range(N)]
        else:
            table = [[random.random() * (x_range[1] - x_range[0]) + x_range[0],
                      random.random() * (y_range[1] - y_range[0]) + y_range[0],
                      random.random() * (w_range[1] - w_range[0]) + w_range[0]] for _ in range(N)]
    else:
        # table = [[0, 1, 100], [2.5, -0.048, 7], [5, -0.178, 5], [7.5, 0.266, 0.1], [10, -0.246, 100]]  # test6
        # table = [[0, -0.648, 1.300], [0.524, -0.576, 1.051], [1.047, -0.074, 8.261], [1.571, 1.290, 51.754],
        #          [2.094, 3.946, 10.285], [2.618, 8.324, 1.378], [3.142, 14.855, 2.233]] # test7
        # table = [[-2, -1, -10.0, 1], [-2, 0, -12.0, 1], [-2, 1, -12.0, 1], [-2, 2, -10.0, 1], [-1, -1, -3.0, 1],
        #          [-1, 0, -4.0, 1], [-1, 1, -3.0, 1], [-1, 2, 0.0, 1], [0, -1, -0.0, 1], [0, 0, 0.0, 1], [0, 1, 2.0, 1],
        #          [0, 2, 6.0, 1], [1, -1, -1.0, 1], [1, 0, 0.0, 1], [1, 1, 3.0, 1], [1, 2, 8.0, 1], [2, -1, -6.0, 1],
        #          [2, 0, -4.0, 1], [2, 1, 0.0, 1], [2, 2, 6.0, 1]] # test8
        table = [[-2, -1, 8.13, 1], [-2, 0, 7.5, 1], [-2, 1, 5.78, 1], [-2, 2, 1.11, 1], [-1, -1, 2.13, 1],
                  [-1, 0, 1.5, 1], [-1, 1, -0.22, 1], [-1, 2, -4.89, 1], [0, -1, 0.13, 1], [0, 0, -0.5, 1],
                  [0, 1, -2.22, 1], [0, 2, -6.89, 1], [1, -1, 2.13, 1], [1, 0, 1.5, 1], [1, 1, -0.22, 1],
                  [1, 2, -4.89, 1], [2, -1, 8.13, 1], [2, 0, 7.5, 1], [2, 1, 5.78, 1], [2, 2, 1.11, 1]]  # test9
        N = len(table)
        x_range = [min(el[0] for el in table), max(el[0] for el in table)]
        y_range = [min(el[1] for el in table), max(el[1] for el in table)]
        if mode == "3d":
            z_range = [min(el[2] for el in table), max(el[2] for el in table)]
    table = sorted(table, key=lambda k: [k[0], k[1]])

    sum1 = 0
    sum2 = 0
    sum3 = 0
    for el in table:
        sum1 += el[0] * el[2]
        sum2 += el[1] * el[2]
        sum3 += el[2]
    avg_x = sum1 / sum3
    avg_y = sum2 / sum3
    print(avg_x, avg_y)

    x, y, z = [], [], []

    if mode == "3d":
        print_3D_table(table)
        for i in (False, True):
            if not i:
                msg = 'Original:'
            else:
                msg = 'Modificational:'
            print(msg)
            fn = approximate_3d(table, n, i)
            for xi in np.linspace(*x_range, count_points):
                for yi in np.linspace(*y_range, count_points):
                    x.append(xi)
                    y.append(yi)
                    z.append(fn(xi, yi))
            fig = plt.figure()
            fig.suptitle(msg)
            ax = fig.add_subplot(projection='3d')
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            ax.plot_trisurf(x, y, z)
            for xi, yi, zi, w in table:
                ax.scatter(xi, yi, zi, c='orange')
            x0 = 0.3
            y0 = -0.2

            print("f({:f}, {:f}) = ".format(x0, y0), fn(x0, y0))
            print()
    else:
        fig = plt.figure()
        ax = fig.add_subplot()
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        print_2D_table(table)
        for i in (2, 3, 6, 20):
            x, y, z = [], [], []
            fn = approximate_2d(table, i)
            for xi in np.linspace(*x_range, count_points):
                x.append(xi)
                y.append(fn(xi))
            ax.plot(x, y, label='n = ' + str(i))

            # x, y, z = [], [], []
            # fn = approximate_2d_y(table, i)
            # for yi in np.linspace(*y_range, count_points):
            #     y.append(yi)
            #     x.append(fn(yi) + avg_x)
            # ax.plot(x, y, label='n = ' + str(i))

        for xi, yi, w in table:
            ax.scatter(xi, yi, c='orange')
        plt.legend()

        # avg_x - table[0][1]
    plt.grid()
    plt.show()


if __name__ == "__main__":
    main()
