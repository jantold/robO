import math
import Robot_Simulator_V3.geometry as geo
import numpy as np
from math import *
from Robot_Simulator_V3 import emptyWorld
from Robot_Simulator_V3 import Robot


# Roboter in einer Welt positionieren:
myWorld = emptyWorld.buildWorld()
myRobot = Robot.Robot()
myWorld.setRobot(myRobot, [2, 5.5, pi / 2])

# Anzahl Zeitschritte n mit jeweils der Laenge T = 0.1 sec definieren.
# T laesst sich ueber die Methode myRobot.setTimeStep(T) einstellen.
# T = 0.1 sec ist voreingestellt.
n = 180

# Definiere Folge von Bewegungsbefehle:
motionCircle = [[0.5, -24 * pi / 180] for i in range(n)]

def straightDrive(v, l):
    motionCircle = [[v, 0 * pi / 180] for i in range(l)]
    for t in range(l):
        # Bewege Roboter
        motion = motionCircle[t]
        print("v = ", motion[0], "omega = ", motion[1] * 180 / pi)
        myRobot.move(motion)
        # Gib Daten vom Distanzsensor aus:
        distanceSensorData = myRobot.sense()
        print("Dist Sensor: ", distanceSensorData)

def abs(x):
    if x >= 0:
        return x
    x = math.sqrt(x ** 2)
    return x

def curveDrive(self, v, r, theta):
    w = v / r
    thetaRad = theta * pi / 180
    omega = w * pi / 180

    if theta >= 0:
        time = round((thetaRad / omega) * 10)
        motionCircle = [[v, omega] for i in range(time)]
    else:
        time = -round((thetaRad / omega) * 10)

        motionCircle = [[v, -omega] for i in range(time)]

    for t in range(time):
        self.move(motionCircle[t])


def goToGlobal(self, p1, p2, v, tol = 0.01):

    running = True
    #while running:

    (x, y, theta2) = myWorld.getTrueRobotPose()
    print(x, y, theta2)
    deltaX = p2[0] - x
    deltaY = p2[1] - y
    theta = np.arctan2(deltaY, deltaX) - theta2
    print("theta: ", theta)
    w = (theta + pi) % (2*pi) - pi
    print("w = ", w)
    if w >= np.radians(1) or w <= np.radians(-1):
        self.move([v / 4, w])
    else:
        self.move([v, w])
    (x, y) = myWorld.getTrueRobotPose()[0:2]
    #if x <= p2[0] + tol and x >= p2[0] - tol and y <= p2[1] + tol and y >= p2[1] - tol:
     #   running = False

def followLine1(self, p1, p2):
    tol = 0.1
    while True:
        polyline = [p1, p2]
        myWorld.drawPolyline(polyline)
        p2_x, p2_y = p2
        pos = self._world.getTrueRobotPose()
        pos_x = pos[0]
        pos_y = pos[1]

        nearest_point = geo.neareastPointOnLine((pos[0], pos[1]), (p1, p2))
        roboP2x = p2_x - nearest_point[0]
        roboP2y = p2_y - nearest_point[1]

        deltaX = nearest_point[0] + roboP2x*0.5

        deltaY = nearest_point[1] + roboP2y*0.5

        goToGlobal(self, p1, [deltaX, deltaY], 0.2)

        if pos_x <= p2[0] + tol and pos_x >= p2[0] - tol and pos_y <= p2[1] + tol and pos_y >= p2[1] - tol:
            break

# Simulation schliessen:
if __name__== "__main__":
    p1 = [10, 12]
    p2 = [1, 15]
    followLine1(myRobot, p1, p2)
    #curveDrive(myRobot, 0.5, 100, 45)
    #straightDrive(0.2, 200)
    myWorld.close()
