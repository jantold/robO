# class Robot.
#
# This class define methods to move a robot
# and to sense the world with a Laser Scanner.
# Distance measurements to landmarks are available.
# Additionally boxes can be sensed, picked up and placed.
#
# The robot does not know its pose!
#
# O. Bittel; 13.09.2019


from math import *
import numpy as np
import random


class Robot:
    # --------
    # init: creates robot.
    #
    def __init__(self):
        self._size = 0.5  # robot diameter
        self._T = 0.1  # time step
        self._world = None  # robot's world; is set by setWorld()

        # Motion noise parameter:
        self._k_d = 0.05 * 0.05  # velocity noise parameter = 0.05m*0.05m / 1m
        self._k_theta = (5.0 * 5.0/360.0) * (pi/180.0)  # turning rate noise parameter = 5deg*5deg/360deg * (1rad/1deg)
        self._k_drift = (2.0 * 2.0)/1.0 * (pi/180.0)**2  # drift noise parameter = 2deg*2deg / 1m
        self._maxSpeed = 1.0 # maximum speed
        self._maxOmega = pi # maximum rotational speed

        # SigmaMotion
        self._SigmaMotion = np.zeros((2,2))

        # Laser Sensor (x-axis is in forward direction):
        self._numberOfBeams = 28
        self._viewAngle = 270.0
        dTheta = self._viewAngle / (self._numberOfBeams - 1)
        self._sensorDirections = [(-135.0 + dTheta * i) * (pi/180.0) for i in range(self._numberOfBeams)]
        self._maxSenseValue = 5.0  # Maximum sensor value for each sensor beam
        self._sensorNoise = 0.01  # standard deviation of distance measurement for 1m

        # Landmark measurement
        self._landmarks = []  # landmark positions
        self._senseNoiseLandmarks = 0.1  # standard deviation of distance measurement

        # Pick and Place Boxes:
        self._boxSensor = True
        self._boxMinSenseValue = 0.2  # Maximum sensor value for each sensor beam
        self._boxMaxSenseValue = 5.0  # Maximum sensor value for each sensor beam
        self._boxDistSensorNoise = 0.01  # standard deviation of distance measurement for 1m
        self._boxAngleSensorNoise = 1*(pi/180)  # standard deviation of angle measurement in rad
        self._boxPlace_x = 0.25  # box place in local x axis
        self._boxPlace_y = 0.0  # box place in local y axis
        self._boxPickUp_x_min = 0.2   # box pick up area in local x axis
        self._boxPickUp_x_max = 0.5   # box pick up area in local x axis
        self._boxPickUp_y_min = -0.1  # box pick up area in local y axis
        self._boxPickUp_y_max = 0.1   # box pick up area in local y axis
        self._boxPickedUp = False
        self._boxInPickUpPosition = False

    def getTimeStep(self):
        return self._T

    def setTimeStep(self, T):
        self._T = T

    # --------
    # returns the diameter of the robot
    #
    def getSize(self):
        return self._size

    # --------
    # returns the direction of the sensors
    #
    def getSensorDirections(self):
        return self._sensorDirections

    # --------
    # returns the maximal possible sensor value
    #
    def getMaxSenseValue(self):
        return self._maxSenseValue


    # --------
    # move the robot for the next time step T by the
    # command motion = [v,omega].
    # Returns False if robot is stalled.
    #
    def move(self, motion):
        v = motion[0]
        omega = motion[1]

        # translational and rotational speed is limited:
        if omega > self._maxOmega:
            omega = self._maxOmega
        if omega < -self._maxOmega:
            omega = -self._maxOmega
        if v > self._maxSpeed:
            v = self._maxSpeed
        if v < -self._maxSpeed:
            v = -self._maxSpeed

        # Add noise to v:
        sigma_v_2 = (self._k_d / self._T) * abs(v)
        v_noisy = v + random.gauss(0.0, sqrt(sigma_v_2))

        # Add noise to omega:
        sigma_omega_tr_2 = (self._k_theta / self._T) * abs(omega)  # turning rate noise
        sigma_omega_drift_2 = (self._k_drift / self._T) * abs(v)  # drift noise
        omega_noisy = omega + random.gauss(0.0, sqrt(sigma_omega_tr_2))
        omega_noisy += random.gauss(0.0, sqrt(sigma_omega_drift_2))

        # Set SigmaMotion:
        self._SigmaMotion[0,0] = sigma_v_2
        self._SigmaMotion[1,1] = sigma_omega_tr_2 + sigma_omega_drift_2

        # Move robot in the world (with noise):
        d_noisy = v_noisy * self._T
        dTheta_noisy = omega_noisy * self._T
        return self._world._moveRobot(d_noisy, dTheta_noisy, self._T)

    # --------
    # returns SigmaMotion from the last move step
    #
    def getSigmaMotion(self):
        return self._SigmaMotion

    # --------
    # sense and returns distance measurements for each sensor beam.
    # If a sensor beams senses no obstacle distance value is set to None.
    #
    def sense(self):
        sensorDistNoisy = []
        sensorDist = self._world._sense()
        for d in sensorDist:
            if d is not None:
                # print "d: ", d
                sigma2 = self._sensorNoise**2 * d
                d += random.gauss(0.0, sqrt(sigma2))
            sensorDistNoisy.append(d)
        return sensorDistNoisy

    # --------
    # returns standard deviation of distance measurement for 1m
    #
    def getSigmaDistSensorNoise(self):
        return self._sensorNoise

    # --------
    # Pick up a box.
    # Only possible if box is in the pick up position
    # and robot has no box already picked up.
    def pickUpBox(self):
        if self._boxPickedUp or not self.boxInPickUpPosition():
            return False
        else:
            if self._world._pickUpBox() != True:
                print("\033[91mError in Robot.pickUpBox")
            self._boxPickedUp = True
            return True

    # --------
    # Pick up a box.
    # Only possible if box is in the pick up position
    # and robot has no box already picked up.
    def placeBox(self):
        if not self._boxPickedUp:
            return True
        self._world._placeBox()
        self._boxPickedUp = False

    # --------
    # Check if a box is in a pick up position.
    def boxInPickUpPosition(self):
        self.senseBoxes()
        return self._boxInPickUpPosition

    # --------
    # Sense boxes.
    # Return [distances, angles] for all sensed boxes.
    # Return None, if no boxes are visible.
    #
    def senseBoxes(self):
        if not self._boxSensor:
            return None

        self._boxInPickUpPosition = False
        distAngle = self._world._senseBox()
        if distAngle is None or distAngle == []:
            return None

        distAngleNoisy = []
        for da in distAngle:
            d = da[0]
            a = da[1]
            if len(da) == 3:
                self._boxInPickUpPosition = True
            sigma2 = self._boxDistSensorNoise**2 * d
            d += random.gauss(0.0, sqrt(sigma2))
            a += random.gauss(0.0, self._boxAngleSensorNoise)
            distAngleNoisy.append((d,a))
        return distAngleNoisy

    # --------
    # returns standard deviation of distance measurement for 1m
    #
    def getSigmaBoxDistSensorNoise(self):
        return self._boxDistSensorNoise

    # --------
    # returns standard deviation of angle measurement in rad
    #
    def getSigmaBoxAngleSensorNoise(self):
        return self._boxAngleSensorNoise

    # --------
    # set world
    #
    def setWorld(self, world):
        self._world = world

    # --------
    # set landmark positions
    #
    def setLandmarks(self, l):
        self._landmarks = l

    # --------
    # return landmark positions
    #

    def getLandmarks(self):
        return self._landmarks

    # --------
    # sense and returns distance measurements to the landmarks
    #
    def senseLandmarks(self):
        z = []  # measurements
        (x,y,_) = self._world.getTrueRobotPose()
        for l in self._landmarks:
            d = sqrt((l[0] - x) ** 2 + (l[1] - y) ** 2)
            d += random.gauss(0.0, self._senseNoiseLandmarks)
            z.append(d)
        return z

    # --------
    # returns Sigma_SenseNoiseLandmarks from the last landmark measurement
    #
    def getSigmaSenseNoiseLandmarks(self):
        n = len(self._landmarks)
        Sigma_SenseNoiseLandmarks = np.zeros((n, n))
        for i in range(n):
            Sigma_SenseNoiseLandmarks[i, i] = self._senseNoiseLandmarks ** 2
        return Sigma_SenseNoiseLandmarks





