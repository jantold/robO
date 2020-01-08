from math import *
from Robot_Simulator_V3 import twoRoomsWorld
from Robot_Simulator_V3 import Robot
import numpy as np


pointerAm = 5

# Roboter in twoRoomWorld positionieren:
myWorld = twoRoomsWorld.buildWorld()
myRobot = Robot.Robot()
myWorld.setRobot(myRobot, [2, 4, 0])


# KeyboardController definieren:
myKeyboardController = myWorld.getKeyboardController()


def wander(self):
    v = 0.5
    dists = [i for i in self.sense() if i is not None]
    length = len(dists)
    mid =  int(length / 2)
    index = dists.index(min(dists))
    if(min(dists) < 0.5 and min(dists) >= 0.3):
        if(index > mid):
            #w = (20 + pi) % (2 * pi) - pi
            self.move([v/4, -0.3])
        else:
            self.move([v/4, 0.3])
    elif(min(dists) < 0.3):
        #w = (45 + pi) % (2 * pi) - pi
        self.move([v/20, 1])
    elif(len(dists) <=3):
        self.move([v, 1])
    else:
        #print("\ndists: ", min(dists))
        w = (0 + pi) % (2*pi) - pi
        self.move([v, w])

def goToGlobal(self, p2, v, tol = 0.1):

    running = True
    while running:

        (x, y, theta2) = myWorld.getTrueRobotPose()
        #print(x, y, theta2)
        deltax = p2[0] - x
        deltay = p2[1] - y
        theta = np.arctan2(deltay, deltax) - theta2
        #print("theta: ", theta)
        w = (theta + pi) % (2*pi) - pi
        #print("w = ", w)
        if w >= np.radians(1) or w <= np.radians(-1):
            self.move([v / 4, w])
        else:
            self.move([v, w])
        (x, y) = myWorld.getTrueRobotPose()[0:2]
        print("x= ", x)
        print ("y= ", y)
        if x <= p2[0] + tol and x >= p2[0] - tol and y <= p2[1] + tol and y >= p2[1] - tol:
            running = False

# Bewege Roboter mit Cursor-Tasten:
def roboMove():
    while True:
        (motion, boxCmd, exit) = myKeyboardController.getCmd()
        # Box operation or move:
        if exit:
            break
        elif boxCmd == 'up':
            myRobot.pickUpBox()
            driveHome(myRobot)
        elif boxCmd == 'down':
            myRobot.placeBox()
        else:
            myRobot.move(motion)
    myWorld.close(False)

def driveHome(self):
    global pointerAm
    betroom1 = [5, 3]
    betroom2 = [9, 3]
    door1 = [14, 10]
    door2 = [16, 10]
    goal = [16, 12]
    if(pointerAm > 3):
        daWay = [betroom1, betroom2, door1, door2, goal]
        for x in daWay:
            goToGlobal(self, x, 0.5)
        self.placeBox()
        for x in reversed(daWay):
            goToGlobal(self, x, 0.5)
    elif(pointerAm ==  3):
        daWay = [betroom1, betroom2, door1, door2, goal]
        for x in daWay:
            goToGlobal(self, x, 0.5)
        self.placeBox()
        daWay.pop(0)
        daWay.pop(0)
        for x in reversed(daWay):
            goToGlobal(self, x, 0.5)

    elif(pointerAm <= 2):
        daWay = [door1, door2, goal]
        for x in daWay:
            goToGlobal(self, x, 0.5)
        self.placeBox()
        for x in reversed(daWay):
            goToGlobal(self, x, 0.5)
    pointerAm = pointerAm - 1
    print("pointerAm = ", pointerAm)


def search(self):
    while True:
        (x, y, theta2) = myWorld.getTrueRobotPose()
        distanceAngles = self.senseBoxes()
        print(distanceAngles)

        #self.move([0.5, w])

        wander(self)
        if(self.boxInPickUpPosition()):
            self.pickUpBox()
            driveHome(self)


if __name__== "__main__":
    search(myRobot)
    #roboMove()

