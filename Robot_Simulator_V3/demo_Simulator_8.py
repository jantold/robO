from Robot_Simulator_V3 import labyrinthWorld
from Robot_Simulator_V3 import Robot
from Robot_Simulator_V3 import sensorUtilities
from math import *
from operator import is_not
from functools import partial

import numpy as np

# Roboter in Office-World positionieren:
myWorld = labyrinthWorld.buildWorld()
myRobot = Robot.Robot()
myWorld.setRobot(myRobot, [2, 18, 0])

# KeyboardController definieren:
myKeyboardController = myWorld.getKeyboardController()

def wander(self):
    while True:
        v = 0.5
        dists = [i for i in self.sense() if i is not None]
        length = len(dists)
        mid =  int(length / 2)
        index = dists.index(min(dists))
        if(min(dists) < 0.5 and min(dists) >= 0.3):
            if(index > mid):
            #w = (20 + pi) % (2 * pi) - pi
                self.move([v/4, -0.5])
            else:
                self.move([v/4, 0.5])
        elif(min(dists) < 0.3):
            #w = (45 + pi) % (2 * pi) - pi
            self.move([v/10, 1])
        else:
            print("\ndists: ", min(dists))
            w = (0 + pi) % (2*pi) - pi
            self.move([v, w])

def followWall(self):
    while True:
        v = 0.5
        dists = [i for i in self.sense() if i is not None]
        if(min(dists) < 0.3 and min(dists) >= 2):
            w = (45 + pi) % (2 * pi) - pi
            self.move([v/20, w])
        else:
            print("\ndists: ", min(dists))
            w = (0 + pi) % (2*pi) - pi
            self.move([v, w])





# Bewege Roboter mit Cursor-Tasten:
def control():
    while True:
        (motion,boxCmd,exit) = myKeyboardController.getCmd()
        if exit:
            break
        myRobot.move(motion)
        dists = myRobot.sense()
        directions = myRobot.getSensorDirections()
        lines_l = sensorUtilities.extractSegmentsFromSensorData(dists, directions)
        lines_g = sensorUtilities.transformPolylinesL2G(lines_l, myWorld.getTrueRobotPose())
        myWorld.drawPolylines(lines_g)

        #print("\nsensordatenLine_l: ", min(lines_l))
        #print("\nsensordatenLine_g: ", min(lines_g))
        print("\ndists: ", min(dists))

    # Simulation schliessen:
    myWorld.close(False)

if __name__== "__main__":
    wander(myRobot)
    #control()
    #followWall(myRobot)

    myWorld.close()
