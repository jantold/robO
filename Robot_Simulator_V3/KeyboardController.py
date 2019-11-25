# class KeyboardController.
#
# O. Bittel; 13.09.2019

from math import *

class KeyboardController:
    def __init__(self, win):
        self.win = win
        self.d_v = 0.1
        self.d_omega = 2.0 * (pi/180.0)
        self.v = 0
        self.omega = 0
        self.v_Max = 1.0
        self.omega_max = 90.0 * (pi/180.0)

    def setDefaultSpeed(self, v, omega):
        self.v = v
        self.omega = omega

    def getCmd(self):
        key = self.win.checkKey()

        if key == "":
            return ((self.v, self.omega), None, False)

        if key == "Escape":
            return (None, None, True)

        boxCmd = None
        if key == "Up":
            if self.v < self.v_Max:
                self.v += self.d_v
        elif key == "Down":
            if self.v > -self.v_Max:
                self.v -= self.d_v
        elif key == "Left":
            if self.omega < self.omega_max:
                self.omega += self.d_omega
        elif key == "Right":
            if self.omega > -self.omega_max:
                self.omega -= self.d_omega
        elif key == "Return":
            self.omega = 0
        elif key == "space":
            self.v = 0
            self.omega = 0
        elif key == "u":
            boxCmd = "up"
        elif key == "d":
            boxCmd = "down"
        return ((self.v, self.omega), boxCmd, False)
