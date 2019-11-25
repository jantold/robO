from math import *
from Robot_Simulator_V3 import twoRoomsWorld
from Robot_Simulator_V3 import Robot


# Roboter in twoRoomWorld positionieren:
myWorld = twoRoomsWorld.buildWorld()
myRobot = Robot.Robot()
myWorld.setRobot(myRobot, [2, 4, 0])


# KeyboardController definieren:
myKeyboardController = myWorld.getKeyboardController()


# Bewege Roboter mit Cursor-Tasten:
while True:
    (motion, boxCmd, exit) = myKeyboardController.getCmd()

    # Box operation or move:
    if exit:
        break
    elif boxCmd == 'up':
        myRobot.pickUpBox()
    elif boxCmd == 'down':
        myRobot.placeBox()
    else:
        myRobot.move(motion)


# Simulation schliessen:
myWorld.close(False)