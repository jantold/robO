# class World.
#
# This class contains methods to define a world and
# to simulate movements and distance sensor measurements of a robot.
# The world consists just of a set of walls (as line segments).
# Only the walls can be seen by the distance sensor of the robot.
# The simulator knows the robot's true pose (getTrueRobotPose).
#
# A set of red boxes can be placed.
# The boxes can be sensed by a box sensor.
#
# Moreover, lines (i.e. planed path) can be drawn in the world.
#
# From the world an occupancy grid can be generated.
#
# Dynamic obstacles lines can be added.
# Unlike simple static world lines they are not considered
# for generating an occupancy grid.
#
# O. Bittel; 12.09.2019


import numpy as np
from math import *
from Robot_Simulator_V3.graphics import *
from Robot_Simulator_V3 import KeyboardController
from Robot_Simulator_V3 import OccupancyGrid
from Robot_Simulator_V3 import geometry


class World:

    # --------
    # init: creates a an empty world
    # with the given size in [m]
    #
    def __init__(self, width, height):
        # World size:
        self._width = width
        self._height = height

        # Border lines:
        self._xll = 0.0 # x coord of left lower point
        self._yll = 0.0 # y coord of left lower point
        self._lines = [] # List of lines
        ll = Point(self._xll, self._yll) # lower left
        lr = Point(self._xll+width, self._yll) # lower right
        ur = Point(self._xll+width, self._yll+height) # upper right
        ul = Point(self._xll, self._yll+height) # upper left
        self._lines.append(Line(ll,lr))
        self._lines.append(Line(lr,ur))
        self._lines.append(Line(ur,ul))
        self._lines.append(Line(ul,ll))

        # Dynamic Obstacles:
        self._dynObstacles = set()
        # dynamic obstacles are defined as world lines (self._lines)
        # The set dynObstacles is used to differentiate obstacle lines
        # from simple static world lines.
        # Data set is used instead of list to make getOccupancyGrid more efficient.

        # Boxes:
        self._boxes = set()
        self._boxSensor = True
        self._boxPickedUp = False
        self._boxSensorAngle = 140 * (pi/180) # 140 degree
        self._boxRadius = 0.1 # box radius
        self._boxesSensedDistAngle = [] # Distance and angles to the sensed boxes

        # Rooms
        self._rooms = []

        # Define graphic window with coordinates and draw borderline
        self._win = GraphWin("HTWG Robot Simulator", int(800.0*width/height), 800, autoflush=False)
        self._win.setCoords(self._xll-0.1, self._yll-0.3, self._xll+width+0.1, self._yll+height+0.1)
        for l in self._lines:
            l.draw(self._win)

        # Robot (initialization is done in setRobot()
        self._robot = None
        self._robotCircle = None # robot is shown as circle with robot position as center
        self._robotTheta = None # robot's global orientation
        self._robotLine = None # local x-axis of the robot

        # Sensor values:
        self._sensorShow = True # Sensor values are shown
        self._sensorDist = [] # Distances to obstacles
        self._sensorPoints = [] # Obstacle points
        self._sensorLines = [] # Sensor beams as lines for drawing

        # Clock:
        self._clockTime = 0.0
        p = Point(self._xll+width/2, self._yll-0.1)
        self._clockTimeText = Text(p,"Clock Time %4.2f" % self._clockTime )
        self._clockTimeText.draw(self._win)

        # Occupancy Grid:
        self._grid = None

        # Distance Grid:
        # Each cell contains the distance to the nearest occupied cell
        self._distanceGrid = None

        # Path history
        self._showPathHistory = False
        self._drivenDistance = 0.0

        # Drawn (several!) polylines:
        self._drawnPolylines = []

    # --------
    # Draw a polyline.
    #
    def drawPolyline(self, polyline, color ='green'):
        self.undrawLines()
        drawn_Polyline = []
        for n in range(len(polyline)-1):
            l = Line(Point(polyline[n][0], polyline[n][1]), Point(polyline[n + 1][0], polyline[n + 1][1]))
            l.draw(self._win)
            l.setFill(color)
            l.setWidth(3)
            drawn_Polyline.append(l)
        self._drawnPolylines.append(drawn_Polyline)

    # --------
    # Draw several polylines.
    #
    def drawPolylines(self, polylines, color='green'):
        self.undrawLines()
        for polyline in polylines:
            drawn_Polyline = []
            for n in range(len(polyline) - 1):
                l = Line(Point(polyline[n][0], polyline[n][1]), Point(polyline[n + 1][0], polyline[n + 1][1]))
                l.draw(self._win)
                l.setFill(color)
                l.setWidth(3)
                drawn_Polyline.append(l)
            self._drawnPolylines.append(drawn_Polyline)

    # # --------
    # # Draw a polyline.
    # #
    # def drawLines(self, lines, color='green'):
    #     self.undrawLines()
    #     for l in lines:
    #         l.draw(self._win)
    #         l.setFill(color)
    #         l.setWidth(3)
    #         self._drawnPolylines.append(l)

    # --------
    # Undraw the polyline.
    #
    def undrawLines(self):
        if self._drawnPolylines == []:
            return
        for polyline in self._drawnPolylines:
            for l in polyline:
                l.undraw()
        self._drawnPolylines = []


    # --------
    # add new a new line from point (x0,y0) to (x1,y1)
    #
    def addLine(self, x0, y0, x1, y1):
        l = Line(Point(x0,y0),Point(x1,y1))
        self._lines.append(l)
        l.setWidth(5)
        l.setFill('blue')
        l.draw(self._win)

    # --------
    # add new a new obstacle line from point (x0,y0) to (x1,y1)
    #
    def addDynObstacleLine(self, x0, y0, x1, y1):
        l = Line(Point(x0,y0),Point(x1,y1))
        self._lines.append(l)
        self._dynObstacles.add(l)
        l.setWidth(10)
        l.setFill('red')
        l.draw(self._win)

    # --------
    # add new a new round Box at point (x,y).
    #
    def addBox(self, x, y):
        box = Circle(Point(x,y),self._boxRadius)
        box.draw(self._win)
        self._boxes.add(box)

    # --------
    # pick up a box if possible.
    #
    def _pickUpBox(self):
        for box in self._boxes:
            if self._boxInPickUpPosition(box):
                self._boxes.remove(box)
                self._boxPickedUp = True
                box.undraw()
                return True
        return False

    # --------
    # pick up a box if possible.
    #
    def _placeBox(self):
        xR = self._robotCircle.getCenter().getX()
        yR = self._robotCircle.getCenter().getY()
        thetaR = self._robotTheta
        c = cos(thetaR)
        s = sin(thetaR)
        x = self._robot._boxPlace_x
        y = self._robot._boxPlace_y
        bgx = xR + c * x - s * y
        bgy = yR + s * x + c * y
        self._boxPickedUp = False
        self.addBox(bgx, bgy)


    def _boxInPickUpPosition(self, box):
        xR = self._robotCircle.getCenter().getX()
        yR = self._robotCircle.getCenter().getY()
        thetaR = self._robotTheta
        c = cos(thetaR)
        s = sin(thetaR)
        x = box.getCenter().getX() - xR
        y = box.getCenter().getY() - yR
        blx = c * x + s * y
        bly = -s * x + c * y
        if blx < self._robot._boxPickUp_x_min or blx > self._robot._boxPickUp_x_max:
            return False
        if bly < self._robot._boxPickUp_y_min or bly > self._robot._boxPickUp_y_max:
            return False
        return True


    # --------
    # Define a new room with name n and center position (x,y).
    #
    def defineRoom(self, n, x, y):
        self._rooms.append([n,x,y])
        t = Text(Point(x,y),n)
        t.draw(self._win)

    # --------
    # Return all rooms.
    #
    def getRooms(self):
        return self._rooms

    # --------
    # set the robot at pose = (x,y,theta) and draw it.
    #
    def setRobot(self, robot, pose):
        x, y, theta = pose
        self._robot = robot
        robot.setWorld(self) # the robot must know his world

        # Check if box sensor:
        self._boxSensor = self._robot._boxSensor

        # Set robot and draw robot:
        c = Point(x,y)
        r = robot.getSize()/2
        self._robotCircle = Circle(c,r)
        self._robotTheta = theta
        p = Point(x+r*cos(theta),y+r*sin(theta))
        self._robotLine = Line(c,p) # line shows the robot's orientation
        self._robotCircle.draw(self._win)
        self._robotLine.draw(self._win)
        self._robotLine.setWidth(3)
        self._drivenDistance = 0.0

        # Update status bar
        self._clockTimeText.setText("Clock Time: %4.2f Driven Distance: %4.2f Position: %4.2f, %4.2f, %4.2f v, omega: %4.2f, %4.2f Picked Up: %r"
                    % (self._clockTime, self._drivenDistance, x, y, theta*180/pi, 0.0, 0.0, False))

        # Show all:
        self._udateWindow()
        print("click in window to start")
        self._win.getMouse() # pause for click in window
        #k = self.win.getKey()
        #print "key "

    # --------
    # get the true robot pose (x,y,theta).
    #
    def getTrueRobotPose(self):
        x = self._robotCircle.getCenter().getX()
        y = self._robotCircle.getCenter().getY()
        theta = self._robotTheta
        return [x,y,theta]

    # --------
    # move the robot in the direction of his self._robotTheta + dTheta/2 by the length of d
    # and then change the robot's orientation by dTheta.
    # The movement takes dt in clock time (dt is only used to change clock time output).
    # If the robot's movement is not possible because of obstacles, the movement will be not
    # performed and False is returned.
    #
    def _moveRobot(self, d, dTheta, dT):
        c = self._robotCircle.getCenter()
        r = self._robotCircle.getRadius()
        x = c.getX()
        y = c.getY()
        theta = self._robotTheta
        dx = d*cos(theta+0.5*dTheta)
        dy = d*sin(theta+0.5*dTheta)
        nc = Point(x+dx,y+dy)

        if self._getNearestDistance(nc) < r: # movement is not possible because of obstacles
            print("Robot stalled: ", x, y, theta)
            # raw_input("Enter: ")
            return False

        # move robot and draw robot:
        self._robotLine.undraw()
        self._robotCircle.move(dx,dy)
        self._robotTheta = (self._robotTheta + dTheta)%(2*pi)
        p = Point(x+dx+r*cos(self._robotTheta),y+dy+r*sin(self._robotTheta))
        self._robotLine = Line(nc,p)
        self._robotLine.draw(self._win)
        self._robotLine.setWidth(3)

        # Path history:
        self._drivenDistance += d
        if self._showPathHistory == True:
            pathLine = Line(c,nc)
            pathLine.setFill('red')
            pathLine.setWidth(3)
            pathLine.draw(self._win)
        #print x+dx, y+dy, self.robotTheta

         # Clear sensor values, compute new sensor values and draw it:
        self._sensorPoints = []
        self._sensorDist = []
        self._sense()
        self._drawSense()
        self._boxesSensedDistAngle = []
        self._senseBox()

        # Update clock and status bar
        self._clockTime += dT
        v = d/dT
        omega = (dTheta/dT)*(180/pi)
        b = self._boxPickedUp
        self._clockTimeText.setText("Clock Time: %4.2f Driven Distance: %4.2f Position: %4.2f, %4.2f, %4.2f v, omega: %4.2f, %4.2f Picked Up: %r"
            % (self._clockTime, self._drivenDistance, x+dx, y+dy, self._robotTheta*180/pi,v,omega,b))

        # show all
        self._udateWindow()
        return True

    # --------
    # Compute distance values in the given direction of the robot sensors
    # If sensorShow = True, sensor beams are displayed.
    #
    def _sense(self):
        if self._sensorDist == []:
            alphas = self._robot.getSensorDirections()
            distMax = self._robot.getMaxSenseValue()
            p = self._robotCircle.getCenter()
            for alpha in alphas:
                theta = (self._robotTheta+alpha) % (2*pi)
                q = self._getNearestIntersectionWithBeam(p, theta)
                #print "p: ", p.getX(), p.getY(), theta
                d = World.__dist(p, q)
                #print "q: ", q.getX(), q.getY(), d
                if d > distMax:
                    self._sensorDist.append(None)
                    x = p.getX()+distMax*cos(theta)
                    y = p.getY()+distMax*sin(theta)
                    self._sensorPoints.append(Point(x,y))
                    #print "sensorPoint: ", x, y, "\n"
                else:
                    self._sensorDist.append(d)
                    self._sensorPoints.append(q)
                    #print "sensorPoint: ", q.getX(), q.getY(), "\n"
            self._drawSense()
            # print "time: ", self._clockTime, time.clock()

        return self._sensorDist


    # --------
    # Draw sensor beams.
    #
    def _drawSense(self):
        if not self._sensorShow:
            return

        # Undraw sensor beam lines:
        for l in self._sensorLines:
            l.undraw()

        # Draw new sensor beam lines:
        self._sensorLines = []
        p = self._robotCircle.getCenter()
        for q in self._sensorPoints:
            l = Line(p,q)
            l.setFill('red')
            self._sensorLines.append(l)
            l.draw(self._win)
        self._robotCircle.undraw()
        self._robotLine.undraw()
        self._robotCircle.draw(self._win)
        self._robotLine.draw(self._win)
        self._robotLine.setWidth(3)

    # --------
    # If boxSensor = True, try to detect box and
    # compute distance and orientation to the detected boxes.
    #
    def _senseBox(self):
        if self._boxSensor == False:
            return None
        if self._boxesSensedDistAngle == []:
            p = self._robotCircle.getCenter()
            dMin = self._robot._boxMinSenseValue
            dMax = self._robot._boxMaxSenseValue
            for box in self._boxes:
                box.undraw()
                box.setFill('white')
                pb = box.getCenter()
                theta = atan2(pb.getY()-p.getY(), pb.getX()-p.getX())
                alphaBox = (self._robotTheta - theta + pi) % (2*pi) - pi
                if abs(alphaBox) <= self._boxSensorAngle/2:
                    d = World.__dist(p, pb)
                    if d >= dMin and d <= dMax:
                        ip = self._getNearestIntersectionWithBeam(p, theta)
                        if World.__dist(p, ip) > d:
                            # Box can be seen:
                            if self._boxInPickUpPosition(box):
                                box.setFill('green')
                                self._boxesSensedDistAngle.append((d,alphaBox, "pickable"))
                            else:
                                box.setFill('red')
                                self._boxesSensedDistAngle.append((d, alphaBox))

                box.draw(self._win)
        return self._boxesSensedDistAngle

    def getKeyboardController(self):
        return KeyboardController.KeyboardController(self._win)

    # --------
    # update and draw the actual window.
    # If simulation runs to fast then delay wth a time.sleep()
    def _udateWindow(self):
        #time.sleep(0.05)
        self._win.update()
        #self.win.getMouse() # pause for click in window


    def close(self, waitForClick = True):
        if waitForClick:
            print("click in window to close")
            self._win.getMouse() # pause for click in window
        self._win.close()


    # --------
    # compute the nearest intersection point between the beam starting at point p in direction of theta
    # and a line of the world
    #
    def _getNearestIntersectionWithBeam(self, p, theta):
        #print "\ntheta= ", theta*180/pi
        if len(self._lines) == 0:
            return None
        dmin = float("inf")
        ip = None
        for line in self._lines:
            #print "line: ", line.getP1().getX(),line.getP1().getY(),line.getP2().getX(),line.getP2().getY()
            q = World._intersectSegmentBeam(p,theta,line)
            if q is not None:
                #print "q =", q.getX(), q.getY(), self._dist(p,q)
                d = World.__dist(p, q)
                if d < dmin:
                    dmin = d
                    ip = q
        if ip is None:
            raise RuntimeError('Beam does not intersect any obstacle. '
                               'Maybe the robot is set outside the world.');
        return ip


    # --------
    # compute the distance to the line of the world which is nearest to p.
    #
    def _getNearestDistance(self, p):
        if len(self._lines) == 0:
            return None
        dmin = float("inf")
        for l in self._lines:
            q = (p.getX(), p.getY())
            v = (l.getP1().getX(), l.getP1().getY())
            w = (l.getP2().getX(), l.getP2().getY())
            d = geometry.distPointSegment(q, (v,w))
            if d < dmin:
                dmin = d
        return dmin


    # --------
    # compute the distance between the points p and q.
    #
    @staticmethod
    def __dist(p, q):
        dx = p.getX()-q.getX()
        dy = p.getY()-q.getY()
        return sqrt(dx*dx+dy*dy)



    # --------
    # Compute the intersection point between segment line and the beam given by p and theta.
    #
    @staticmethod
    def _intersectSegmentBeam(p, theta, line):
        x0 = p.getX()
        y0 = p.getY()
        x1 = line.getP1().getX()
        y1 = line.getP1().getY()
        x2 = line.getP2().getX()
        y2 = line.getP2().getY()
        q = geometry.intersectRaySegment(((x0,y0),theta), ((x1,y1), (x2,y2)))
        if q == None:
            return None
        else:
            (qx, qy) = q
            ip = Point(qx,qy)
        return ip


    def getOccupancyGrid(self, cellSize = 0.1):
        if self._grid is None:
            self._grid = self._generateOccupancyGrid(cellSize)
        return self._grid


    def _generateOccupancyGrid(self, cellSize = 0.1):
        grid = OccupancyGrid.OccupancyGrid(self._xll, self._yll, self._width, self._height, cellSize)
        for l in self._lines:
            # Note: element check is done by reference.
            # This is valid, since each line is constructed only once.
            if l in self._dynObstacles:
                continue
            x0 = l.getP1().getX()
            y0 = l.getP1().getY()
            x1 = l.getP2().getX()
            y1 = l.getP2().getY()
            grid._addLine(x0, y0, x1, y1)
        return grid


    def getDistanceGrid(self, cellSize=0.1):
        if self._distanceGrid is None:
            self._distanceGrid = self._generateOccupancyGrid(cellSize)
            self._distanceGrid._extendToDistanceGrid()
        return self._distanceGrid










