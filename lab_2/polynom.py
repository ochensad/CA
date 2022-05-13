from copy import deepcopy
import numpy as np
import utils.consts as names 
from func import getTypeOfMonotone
from utils.default import getClosestPoints, printTableRound, bubble

def NewtonMethod(table):    
    countOfRowsOfTableData = 2
    tableOfSub = [[x, y] for [x, y] in table]
    tableOfSub = list([list(row) for row in np.transpose(tableOfSub)])
    XRow = tableOfSub[0]
    # Добавление столбцов (строк в моей реализации)
    for countOfArgs in range(1, len(XRow)):
        tableOfSub.append([])
        curYRow = tableOfSub[len(tableOfSub) - countOfRowsOfTableData]
        # Добавление очередного элемента
        for j in range(0, len(XRow) - countOfArgs):
            cur = (curYRow[j] - curYRow[j + 1]) / (XRow[j] - XRow[j + countOfArgs])
            tableOfSub[countOfArgs + countOfRowsOfTableData - 1].append(cur)
    return tableOfSub

def ErmitMethod(table):
    countOfRowsOfTableData = 2
    tableOfSub = [[x, y] for [x, y, yd] in table]
    YdRow = []
    for [_, _, yd] in table:
        YdRow.append(yd)
        YdRow.append(None)
    XColId = 0
    YColId = 1
    # Вставка пустых списком (будущих разностей) в 3 столбец
    for i in range(0, len(tableOfSub) * 2, 2): tableOfSub.insert(i + 1, [])
    # Копирование точек
    for i in range(0, len(tableOfSub), 2):
        tableOfSub[i + 1].append(tableOfSub[i][XColId])
        tableOfSub[i + 1].append(tableOfSub[i][YColId])
    for i in range(0, len(tableOfSub) - 2, 2):
        subElement = (tableOfSub[i][YColId] - tableOfSub[i + 2][YColId]) / (tableOfSub[i][XColId] - tableOfSub[i + 2][XColId])
        YdRow[i + 1] = subElement
    tableOfSub = list([list(row) for row in np.transpose(tableOfSub)])
    XRow = tableOfSub[0]
    YdRow.pop()
    tableOfSub.append(YdRow)

    # Добавление столбцов (строк в моей реализации)
    for countOfArgs in range(2, len(XRow)):
        tableOfSub.append([])
        curYRow = tableOfSub[len(tableOfSub) - countOfRowsOfTableData]
        # Добавление очередного элемента
        for j in range(0, len(XRow) - countOfArgs):
            if (abs(XRow[j] - XRow[j + countOfArgs]) < 1e-8):
                cur = YdRow[j]
            else:
                cur = (curYRow[j] - curYRow[j + 1]) / (XRow[j] - XRow[j + countOfArgs])
            tableOfSub[countOfArgs + countOfRowsOfTableData - 1].append(cur)
    # Удаление пустого списка
    return tableOfSub

def calcApproximateValue(tableOfSub, n, x):
    countOfArgs = 2
    sum = tableOfSub[1][0]
    mainPart = 1
    for i in range(n):
        mainPart *= (x - tableOfSub[0][i])
        sum += mainPart * tableOfSub[i + countOfArgs][0]
    return sum

def createTableOfSub(table, mode):
    if mode == names.NEWTON:
        return NewtonMethod(table)
    else:
        return ErmitMethod(table)

def findRoot(table, n, mode, monotone):
    copyTable = [row.copy() for row in table]
    if mode == names.NEWTON and monotone != names.NOTMONOTONE: 
        for row in copyTable:
            row[0], row[1] = row[1], row[0]
        tableOfSub = createTableOfSub(copyTable, mode)
        return calcApproximateValue(tableOfSub, n, 0)
    elif (mode == names.ERMIT) or (mode == names.NEWTON and monotone == names.NOTMONOTONE):
        tableOfSub = createTableOfSub(table, mode)
        r = table[-1][0]
        l = table[0][0]
        while r - l > 1e-8:
            m = (r + l) / 2
            y = calcApproximateValue(tableOfSub, n, m)
            if y < 0:
                l = m
            else:
                r = m
        return l

def getApproximateValueFromTable(table, x, mode, n):
    table = bubble(table)
    monotone = None
    monotone = getTypeOfMonotone(table)
    if mode == names.NEWTON:
        table = getClosestPoints(table, n + 1, x, monotone)
    else:
        table = getClosestPoints(table, n, x, monotone)
    monotone = getTypeOfMonotone(table)
    # задуматься над вышенаписанным
    tableOfSub = createTableOfSub(table, mode)
    return calcApproximateValue(tableOfSub, n, x)

def getApproximateValueFrom3DMatrix(data, nx, ny, nz, mode, xP, yP, zP):
    m = data['matrix']
    xArr = data['xValues']
    yArr = data['yValues']
    zArr = data['zValues']
    zTable = []
    for zi, z in enumerate(zArr):
        yTable = []
        for yi, y in enumerate(yArr):
            xTable = []
            # print('\n',y)
            for xi, x in enumerate(xArr):
                el = [x, m[xi][yi][zi]]
                # print(el)
                xTable.append(deepcopy(el))
            # print(names.f(xP, y, zArr[3]))
            yTable.append(
                [y, getApproximateValueFromTable(xTable, xP, mode, nx)]
            )
        zTable.append(
            [z, getApproximateValueFromTable(yTable, yP, mode, ny)]
        )
    # print(zTable)
    return getApproximateValueFromTable(zTable, zP, mode, nz)