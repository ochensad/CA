import utils.consts as names

def getTypeOfMonotone(table):
    isIncreasing = True
    isDecreasing = True
    for rowI in range(len(table) - 1):
        if not (table[rowI][1] < table[rowI + 1][1] and table[rowI][0] < table[rowI + 1][0]):
            isIncreasing = False
    for rowI in range(len(table) - 1):
        if not (table[rowI][1] > table[rowI + 1][1] and table[rowI][0] > table[rowI + 1][0]):
            isDecreasing = False
    if isIncreasing:
        return names.INCREASING
    if isDecreasing:
        return names.DECREASING
    return names.NOTMONOTONE