from math import *
from Robot_Simulator_V3 import obstacleWorld3
from Robot_Simulator_V3 import Robot


# Roboter in obstacleWorld3 positionieren:
myWorld = obstacleWorld3.buildWorld()
myRobot = Robot.Robot()
myWorld.setRobot(myRobot, [1, 6, 0])

# Polygonzug, der abgefahren werden soll, einzeichnen:
polyline = [[1,6],[9.5,6],[10.5,3]]
myWorld.drawPolyline(polyline)


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