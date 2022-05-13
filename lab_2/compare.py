from polynom import getApproximateValueFrom3DMatrix
from utils.default import readTable, read3DMatrix, f
from utils.consts import NEWTON

ns = [1, 2, 3]
inputTable = read3DMatrix("./tests/data_8.txt")

print('\nNs:            {:20} {:20} {:20} '.format(*ns))
for n1 in ns:
    print("x =", n1)
    for n2 in ns:
        print(" " * 15, end='')
        for n3 in ns:
            x = 8.3
            y = 4.7
            z = 5
            mode = NEWTON
            nx = n1
            ny = n2
            nz = n3
            matrixData = read3DMatrix('./tests/data_8.txt')
            v = getApproximateValueFrom3DMatrix(matrixData, nx, ny, nz, mode, x, y, z)
            print("{:20}".format(v), end=' ')
        print()
    print()
# print('\nFactional\n')
# print('\nNs:            {:20} {:20} {:20} '.format(*ns))
# for n1 in ns:
#     print("x =", n1)
#     for n2 in ns:
#         print(" " * 15, end='')
#         for n3 in ns:
#             x = 8.3
#             y = 4.7
#             z = 5
#             mode = NEWTON
#             nx = n1
#             ny = n2
#             nz = n3
#             matrixData = read3DMatrix('./tests/data_8.txt')
#             v = f(x, y, z)
#             print("{:20}".format(v), end=' ')
#         print()
#     print()