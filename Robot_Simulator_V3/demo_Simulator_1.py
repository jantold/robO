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
n = 200

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


def curveDrive(v, r, delt0):
    motionCircle = [[v, r * pi / 180] for i in range(delt0)]
    for t in range(delt0):
        # Bewege Roboter
        motion = motionCircle[t]
        print("v = ", motion[0], "omega = ", motion[1] * 180 / pi)
        myRobot.move(motion)
        # Gib Daten vom Distanzsensor aus:
        distanceSensorData = myRobot.sense()
        print("Dist Sensor: ", distanceSensorData)

# Bewege Roboter
#for t in range(n):
#    # Bewege Roboter
#    motion = motionCircle[t]
#    motion = straightDrive(0.5, 500)
#    print("v = ", motion[0], "omega = ", motion[1] * 180 / pi)
#    myRobot.move(motion)
#
    # Gib Daten vom Distanzsensor aus:
#    distanceSensorData = myRobot.sense()
#    print("Dist Sensor: ", distanceSensorData)

    # Simulation schliessen:
if __name__== "__main__":
    straightDrive(0.5, 50)
    curveDrive(0.2, -24,50)
    curveDrive(0.2, 24, 50)
    straightDrive(0.5, 50)
    curveDrive(0.2, -20, 50)
    straightDrive(0.5, 50)
    curveDrive(0.2, -20, 50)
    straightDrive(0.5, 50)
    curveDrive(0.2, -20, 50)
    straightDrive(0.5, 50)
    curveDrive(0.2, -20, 50)
    straightDrive(0.5, 100)

    #curveDrive(0.5, 24, 20)
    #straightDrive(0.2, 200)
    myWorld.close()
