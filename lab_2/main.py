from polynom import getApproximateValueFrom3DMatrix
from utils.default import read3DMatrix
import utils.consts as names

def main():
    x = 0.5
    y = 0.5
    z = 0.05
    mode = names.NEWTON
    nx = 2
    ny = 3
    nz = 2
    matrixData = read3DMatrix('./tests/task_data.txt')
    # matrixData = read3DMatrix('./tests/task_data.txt')
    res = getApproximateValueFrom3DMatrix(matrixData, nx, ny, nz, mode, x, y, z)
    print("Result:", res)
    print("F(x, y, z):", names.f(x, y, z))

if __name__ == '__main__':
    main()
