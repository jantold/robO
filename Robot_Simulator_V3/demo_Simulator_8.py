from Robot_Simulator_V3 import labyrinthWorld
from Robot_Simulator_V3 import Robot
from Robot_Simulator_V3 import sensorUtilities


# Roboter in Office-World positionieren:
myWorld = labyrinthWorld.buildWorld()
myRobot = Robot.Robot()
myWorld.setRobot(myRobot, [2, 18, 0])

# KeyboardController definieren:
myKeyboardController = myWorld.getKeyboardController()


# Bewege Roboter mit Cursor-Tasten:
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

# Simulation schliessen:
myWorld.close(False)