from sre_constants import IN
import numpy as np
# from .consts import *
from .consts import *
from copy import deepcopy
import re

# def npcopy(arr):
#     return np.array(deepcopy(arr))

def bubble(table):
    res = deepcopy(table)
    for i in range(len(res)):
        for j in range(len(res) - 1):
            if res[j][0] > res[j + 1][0]:
                res[j], res[j + 1] = res[j + 1], res[j]
    return res

def printTable(table):
    for row in table:
        print(row)

def getClosestPoints(table, n, x, monotone):
    closestI = 0
    if monotone == INCREASING or monotone == NOTMONOTONE:
        for i in range(1, len(table)):
            if table[i][0] > x:
                closestI = i
                break
    elif monotone == DECREASING:
        for i in range(1, len(table)):
            if table[i][0] < x:
                closestI = i
                break
    else:
        print("getClosestPoints error")
    countR = n // 2
    countL = n - countR
    if closestI - countL < 0 and closestI + countR > len(table):
        return deepcopy(table)
    if closestI - countL < 0:
        return table[0: closestI + countR + abs(closestI - countL)]
    if closestI + countR > len(table):
        return table[closestI - countL + (len(table) - closestI - countR):]
    return table[closestI - countL: closestI + countR]

def readTable(filename):
    table = []
    file = open(filename)
    for line in file.readlines():
        row = list(map(float, line.split(" ")))
        table.append(row)
    file.close()
    return table

def printTableRound(table):
    for row in table:
        resRow = list(map(lambda el: round(el, 4), row))
        print(resRow)

def parseFloat(s):
    return float(re.findall("-?\d+\.?\d*", s)[0]) 

def read3DMatrix(filename):
    def isZRow(row):
        return 'z' in row[0]
    def isEmptyRow(row):
        return row[0] == '\n'
    zValues = []
    matrix = []
    layer = []
    file = open(filename)
    for row in file.readlines():
        if isEmptyRow(row):
            matrix.append(deepcopy(layer))
            layer = []
            continue
        row = row.strip()
        if isZRow(row):
            zValues.append(parseFloat(row))
            continue
        rowArr = row.split(' ')
        for i, num in enumerate(rowArr):
            try: rowArr[i] = float(num)
            except Exception: rowArr[i] = 0
        layer.append(deepcopy(rowArr))
    file.close()
    matrix = np.array(matrix)
    xValues = deepcopy([float(i) for i in matrix[0][0][1:]])
    yValues = deepcopy([float(i) for i in matrix[0][:,0][1:]])
    zValues = [float(i) for i in zValues]
    matrix = np.swapaxes(matrix[0:,1:,1:], 0, 2)
    return {
        "matrix": matrix,
        "xValues": xValues,
        "yValues": yValues,
        "zValues": zValues,
    }

if __name__ == '__main__':
    res = readTable('./tests/data_6.txt')
    res = getClosestPoints(res, 7, 170.1, DECREASING)
    printTable(res)