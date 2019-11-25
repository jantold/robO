import numpy as np
import numpy.linalg as la

def translation(t):
    if len(t) == 2:
        array = np.array([[t[0]],[t[1]]])
        matrix = np.identity(2)
        tram = np.hstack((matrix,array))
        tram = np.vstack((tram, [0,0,1]))

    if len(t) == 3:
        array = np.array([[t[0]],[t[1]],[t[2]]])
        matrix = np.identity(3)
        tram = np.hstack((matrix,array))
        tram = np.vstack((tram, [0,0,0,1]))
    return tram

def rot2trans(r):
    dreiDRow = np.array([0,0,0])
    if r.shape == (3,3):
        homRot = np.vstack([r, dreiDRow])
        homRot = np.hstack([homRot, [[0],[0],[0],[1]]])
    else:
        homRot = np.vstack((r, [0,0]))
        homRot = np.hstack((homRot, [[0],[0],[1]]))
    return homRot

def rotx(theta):
    theta = np.radians(theta)
    matrix3d = np.array([[1, 0, 0], [0, np.cos(theta), -np.sin(theta)], [0, np.sin(theta), np.cos(theta)]])
    return matrix3d

def roty(theta):
    theta = np.radians(theta)
    matrix3d = np.array([[np.cos(theta), 0, np.sin(theta)], [0, 1, 0], [-np.sin(theta), 0, np.cos(theta)]])
    return matrix3d

def rotz(theta):
    theta = np.radians(theta)
    matrix3d = np.array([[np.cos(theta), -np.sin(theta), 0], [np.sin(theta), np.cos(theta), 0], [0, 0, 1]])
    return matrix3d

def dhkon(d1,zrot,a1,xrot):
    Tld = translation([0,0,d1])
    Rz = rot2trans(rotz(zrot))
    Tla1 = translation(a1,0,0)
    Rx = rot2trans(rotx(xrot))
    matrix = np.dot(Tld, Rz)
    matrix = np.dot(matrix, Tla1)
    matrix = np.dot(matrix, Rx)
    return matrix

def greifarmkinematik():
    #first = dhkon(0.35,30,2.25,0)
    #second = dhkon(0,40,0,0)
    #third = translation([0, -0.05, 0])
    #fourth = dhkon(0,0,0.5,-30)
    #fift = dhkon(0,0,0.5,10)

    #finalmatrix = np.dot(first,second)
    #finalmatrix = np.dot(finalmatrix,third)
    #finalmatrix = np.dot(finalmatrix,fourth)
    #finalmatrix = np.dot(finalmatrix,fift)
    #finalmatrix = np.dot(finalmatrix,(0,0,0,1))

    #print("\n", finalmatrix)


    matrix0 = translation([2,1,0.1])
    print("\n",matrix0)
    matrix1 = rotz(30)
    matrix1 = rot2trans(matrix1)
    print("\n",matrix1)
    matrix2 = translation([0.25,0,0.25])
    print("\n", matrix2)
    matrix4 = rotz(40)
    matrix4 = rot2trans(matrix4)
    print("\n", matrix4)
    matrixY = translation([0,-0.05,0])
    matrixB1 = roty(-30)
    matrixB1 = rot2trans(matrixB1)
    print("\n", matrixB1)
    matrixl1 = translation([0.5,0,0])
    print("\n", matrixl1)
    matrixB2 = roty(10)
    matrixB2 = rot2trans(matrixB2)
    print("\n", matrixB2)
    matrixl2 = translation([0.5,0,0])
    print("\n", matrixl2)



    newMatrix = np.dot(matrix0, matrix1)
    newMatrix = np.dot(newMatrix,matrix2)
    newMatrix = np.dot(newMatrix, matrix4)
    newMatrix = np.dot(newMatrix,matrixY)
    newMatrix = np.dot(newMatrix, matrixB1)
    newMatrix = np.dot(newMatrix, matrixl1)
    newMatrix = np.dot(newMatrix, matrixB2)
    newMatrix = np.dot(newMatrix, matrixl2)
    print("\n", newMatrix)
    newMatrix = np.dot(newMatrix,(0,0,0,1))
    print("\n", newMatrix)

if __name__ == '__main__':
    greifarmkinematik()