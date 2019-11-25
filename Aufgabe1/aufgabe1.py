import numpy as np
import numpy.linalg as la

def rot(theta):
    theta = np.radians(theta)
    matrix2d = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    #print("theta =",theta)
    return matrix2d


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

def rot2trans(r):
    dreiDRow = np.array([0,0,0])
    zweiDRow = np.array([0,0])
    if r.shape == (3,3):
        homRot = np.vstack([r, dreiDRow])
        homRot = np.hstack([homRot, [[0],[0],[0],[1]]])
    else:
        homRot = np.vstack((r, [0,0]))
        homRot = np.hstack((homRot, [[0],[0],[1]]))
    return homRot

def trans(t):
    if len(t) == 2:
        array = np.array([[t[0]],[t[1]]])
        matrix = np.identity(2)
        tram = np.hstack((matrix,array))
        tram = np.vstack((tram, [0,0,1]))

        return tram
    if len(t) == 3:
        array = np.array([[t[0]],[t[1]],[t[2]]])
        matrix = np.identity(3)
        tram = np.hstack((matrix,array))
        tram = np.vstack((tram, [0,0,0,1]))
        return tram


if __name__ == '__main__':
    array1 = np.array([1,1,1])
    t1 = np.array([1,1])
    t2 = np.array([2,2,2])
    print(rot(30))
    print("rotx =\n", rotx(30))
    print("roty =\n", roty(30))
    print("rotz =\n", rotz(30))
    print("homogoene Transformationsmatrix:\n", rot2trans(np.identity(3)))
    print("\nhomogene Translationsmatrix\n", trans(t2))
