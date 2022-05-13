import random
import sys
import json

import numpy as np
from matplotlib import pyplot as plt


def approximate_1d(func_table, n=1):
    a = [
        [
            sum(list(map(lambda row: row[0] ** (i + j) * row[2], func_table)))
            for j in range(n + 1)
        ] for i in range(n + 1)
    ]
    b = [
        sum(list(map(lambda row: row[0] ** i * row[1] * row[2], func_table)))
        for i in
        range(n + 1)
    ]
    c = list(np.linalg.solve(a, b))

    def approx_func(x):
        result = 0
        x_degree = 1
        for ci in c:
            result += x_degree * ci
            x_degree *= x
        return result

    return approx_func

def getValue(x, y, powx, powy):
    return x**powx * np.exp(y) ** powy

def approximate_2d(func_table, n=1):
    a = []
    b = []
    for i in range(n + 1):
        for j in range(n + 1 - i):
            a_row = []
            for k in range(n + 1):
                for t in range(n + 1 - k):
                    a_row.append(sum(
                        list(
                            map(
                                lambda row: getValue(row[0], row[1], k + i, t + j)#row[0] ** (k + i) * row[1] ** (
                                        #t + j)
                    * row[3],
                                func_table
                            )
                        )
                    ))
            a.append(a_row)
            b.append(
                sum(
                    list(
                        map(
                            lambda row: getValue(row[0], row[1], i, j)# *row[0] ** i * row[1] ** j
                                        * row[2] *
                                        row[3],
                            func_table
                        )
                    )
                )
            )

    for i in a:
        print(i)
    c = list(np.linalg.solve(a, b))

    def approx_func(x, y):
        result = 0
        x_degree = 0
        c_index = 0
        for i in range(n + 1):
            y_degree = 0
            for j in range(n + 1 - i):
                result += c[c_index] * getValue(x, y, x_degree, y_degree)
                y_degree += 1
                c_index += 1
            x_degree += 1
        return result

    return approx_func
def swap_index(i1, i2, table):
    for i in table:
        i[i1], i[i2] = i[i2], i[i1]

def main(input_filename):
    x_limits = [-5, 5]
    y_limits = [-15, 15]
    z_limits = [-6, 16]
    w_limits = [0, 1]
    points_for_func = 100
    with open(input_filename, "r") as input_file:
        data = json.loads(input_file.read())
    x_limits = data.get("x_limits", x_limits)
    y_limits = data.get("y_limits", y_limits)
    z_limits = data.get("z_limits", z_limits)

    filename = "C:\dev\study\PyVICHALG\lab_04\in9"

    if data["mode"] == "3d":
        func_data = []
        with open(filename, "r") as f_in:
            for line in f_in:
                if not "//" in line:
                    func_data.append(list(map(lambda num: float(num), line.split())))
        swap_index(0, 1, func_data)
        swap_index(1, 2, func_data)
    else:
        func_data = []
        with open(filename, "r") as f_in:
            for line in f_in:
                if not "//" in line:
                    func_data.append(list(map(lambda num: float(num), line.split())))
    print(func_data)
    if data["mode"] == "3d":
        fn = approximate_2d(func_data, data["n"])
    else:
        fn = approximate_1d(func_data, data["n"])

    print(fn(0.3, -0.2))
    # fig = plt.figure()
    # ax = fig.add_subplot(projection='3d' if data["mode"] == "3d" else None)
    # ax.set_xlabel('X')
    # ax.set_ylabel('Y')
    # if data["mode"] == "3d":
    #     ax.set_zlabel('Z')
    # x = []
    # y = []
    # z = []
    # x_limits = [func_data[0][0], func_data[len(func_data) - 1][0]]
    # y_limits = [func_data[0][1], func_data[len(func_data) - 1][1]]
    # for xi in np.linspace(*x_limits, points_for_func):
    #     if data["mode"] == "3d":
    #         for yi in np.linspace(*y_limits, points_for_func):
    #             x.append(xi)
    #             y.append(yi)
    #             z.append(fn(xi, yi))
    #     else:
    #         x.append(xi)
    #         y.append(fn(xi))
    # if data["mode"] == "3d":
    #     ax.plot_trisurf(x, y, z)
    #     for xi, yi, zi, w in func_data:
    #         ax.scatter(xi, yi, zi)
    # else:
    #     ax.plot(x, y)
    #     for xi, yi, w in func_data:
    #         ax.scatter(xi, yi)
    # plt.show()


if __name__ == "__main__":
    main("input.json")
