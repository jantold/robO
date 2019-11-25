from math import *
from Robot_Simulator_V3 import obstacleWorld3
from Robot_Simulator_V3 import Robot


# Roboter in obstacleWorld3 positionieren:
myWorld = obstacleWorld3.buildWorld()
myRobot = Robot.Robot()
myWorld.setRobot(myRobot, [11.7, 6, 0])

# KeyboardController definieren:
myKeyboardController = myWorld.getKeyboardController()


# Bewegunsfolge für s = 1m vorwärts fahren:
s = 1.0 # m
v = 0.2 # m/s
n = int((s/v)/myRobot.getTimeStep()) # Zeitschritte
print(n)
motionList = [[v, 0] for i in range(n)] # Bewegungsbefehle

# Bewege Roboter vorwärts:
for t in range(n):
    # Bewege Roboter
    motion = motionList[t]
    myRobot.move(motion)

# Pick up
if myRobot.boxInPickUpPosition():
    print("Pick up box")
    myRobot.pickUpBox()

# Warte n Schritte:
for t in range(n):
    myRobot.move([0,0])

# Bewege Roboter vorwärts:
for t in range(n):
    # Bewege Roboter
    motion = motionList[t]
    myRobot.move(motion)

# Pick up:
myRobot.placeBox()
print("Place box")

# Warte n Schritte:
for t in range(n):
    myRobot.move([0,0])

# Simulation schliessen:
myWorld.close()