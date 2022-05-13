from copy import deepcopy
import math
from consts import f, df
import numpy as np

def createTableData():
    # begin = 101.5 # data_3
    # end = 103.4
    # step = 0.25
    begin = 167 # data_4
    end = 174
    step = 0.25
    # begin = 2.25 # data_5
    # end = 4.25
    # step = 0.25

    result = []
    x = begin
    while x + 1e-8 < end:
        result.append([x, f(x), df(x)])
        x += step

    file = open('./tests/data_4.txt', 'w')
    for point in result:
        row = "{} {} {}\n".format(point[0], point[1], point[2])
        file.write(row)

    file.close()

def create3DMatrixData():
    bx = -1
    ex = 1
    by = -1
    ey = 1
    bz = -1
    ez = 1
    step = 0.5
    file = open('./tests/data_8.txt', 'w')
    # xs = list(range(bx, ex))
    # ys = list(range(by, ey))
    # zs = list(range(bz, ez))
    xs = list(np.linspace(bx, ex, 5))
    ys = list(np.linspace(by, ey, 5))
    zs = list(np.linspace(bz, ez, 5))
    for z in zs:
        file.write('\t\t\t\t\tz=' + str(z) +'\n')
        file.write("y/x " + " ".join([str(i) for i in xs]))
        file.write('\n')
        for index, y in enumerate(ys):
            curRow = [ys[index]]
            for x in xs:
                curRow.append(f(x, y, z))
            file.write(" ".join([str(round(i, 2)) for i in curRow]))
            file.write("\n")
        file.write('\n')
            
            
    file.close()

create3DMatrixData()