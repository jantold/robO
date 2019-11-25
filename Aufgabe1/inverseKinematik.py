import numpy as np
import numpy.linalg as la
import math
def rotx(theta):
    theta = np.radians(theta)
    matrix3d = np.array([[1, 0, 0], [0, np.cos(theta), -np.sin(theta)], [0, np.sin(theta), np.cos(theta)]])
    return matrix3d

def rot2trans(r):
    dreiDRow = np.array([0,0,0])
    if r.shape == (3,3):
        homRot = np.vstack([r, dreiDRow])
        homRot = np.hstack([homRot, [[0],[0],[0],[1]]])
    else:
        homRot = np.vstack((r, [0,0]))
        homRot = np.hstack((homRot, [[0],[0],[1]]))
    return homRot

def roty(theta):
    theta = np.radians(theta)
    matrix3d = np.array([[np.cos(theta), 0, np.sin(theta)], [0, 1, 0], [-np.sin(theta), 0, np.cos(theta)]])
    return matrix3d

def rotz(theta):
    theta = np.radians(theta)
    matrix3d = np.array([[np.cos(theta), -np.sin(theta), 0], [np.sin(theta), np.cos(theta), 0], [0, 0, 1]])
    return matrix3d

def lengthA(x, b):
    a = np.sqrt((x**2) + (b**2))
    return a

def lengthC(a, a1, a2):
    c = ((a**2) - (a1**2) - (a2**2))/2*a1;
    return c

def lengthB(epsi, a2, c):
    b = epsi * np.sqrt((a2**2) - (c**2))
    return b

import numpy as np

print("Aufgabe 2a:\n")


def greifarm():
    l = 0.6
    l1 = 0.5
    l2 = 0.5
    h = 0.2
    r = 0.1
    a = 0.1
    b = 0.1
    alpha = 40
    beta = 30
    beta2 = -10

    tv_0_r = np.array([[2], [1], [r]])
    t_0_r = np.dot(trans(tv_0_r), rot2trans(rotz(30)))

    tv_r_db = np.array([[l / 2 - a / 2], [0], [h]])
    t_r_db = trans(tv_r_db)

    tv_db_d = np.array([[0], [0], [b / 2]])
    t_db_d = np.dot(np.dot(trans(tv_db_d), rot2trans(a1.rotz(alpha))), rot2trans(rotx(90)))

    tv_d_a1 = np.array([[0], [0], [a / 2]])
    tl_l = np.array([[l1], [0], [0]])
    t_d_a1 = np.dot(np.dot(trans(tv_d_a1), rot2trans(a1.rotz(beta))), trans(tl_l))

    tv_a1_a2 = np.array([[l2], [0], [0]])
    t_a1_a2 = np.dot(a1.rot2trans(rotz(beta2)), trans(tv_a1_a2))

    matrix = np.dot(t_0_r, t_r_db)
    matrix = np.dot(matrix, t_db_d)
    matrix = np.dot(matrix, t_d_a1)
    matrix = np.dot(matrix, t_a1_a2)
    p0 = np.dot(matrix, (0, 0, 0, 1))

    print("\n", t_0_r)
    print("\n", t_r_db)
    print("\n", t_db_d)
    print("\n", t_d_a1)
    print("\n", t_a1_a2)
    print(p0)


if __name__ == '__main__':
    a = 0
    b = 0
    l1 = 0.6
    l2 = 0.5

    B = lengthB(-1, 0.5, lengthC(lengthA(0.9916,0.62101007), l1, l2))
    C = lengthC(lengthA(0.9028,0.62101007), l1, l2)

    omega2 = np.degrees(np.arctan2(B, C))
    alpha = np.degrees(np.arctan2(0.58034659,0.99163013-(l1/2)))
    print("\n alpha:", alpha)
    print("\nomega2:" , omega2)
    print("\n", lengthA(0.9028, 0.4210))