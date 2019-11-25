from math import *
from Robot_Simulator_V3 import officeWorld
from Robot_Simulator_V3 import Robot


# Roboter in Office-World positionieren:
myWorld = officeWorld.buildWorld()
myRobot = Robot.Robot()
myWorld.setRobot(myRobot, [2, 5.5, pi/2])

# KeyboardController definieren:
myKeyboardController = myWorld.getKeyboardController()


# Bewege Roboter mit Cursor-Tasten:
while True:
    (motion,boxCmd,exit) = myKeyboardController.getCmd()
    if exit:
        break
    myRobot.move(motion)

# Simulation schliessen:
myWorld.close(False)