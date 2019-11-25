# class OccupancyGrid.
#
# This class define methods to construct an occupancy grid.
#
# The grid cells can be set with addLine and setValue.
# Grid cell values can be get with getValue.
#
# The occupancy grid can be extended to a distance grid with extendToDistanceGrid().
#
# An occupancy grid can be drawn in black and white.
# A distant grid can be drawn in grey scales.
#
# O. Bittel
# AIN V1.1; 04.12.2017

from Robot_Simulator_V3.graphics import *
import heapq

class OccupancyGrid:

    # --------
    # init: creates a an empty occupancy grid with the given cell size
    #
    def __init__(self, xll, yll, width, height, cellSize = 0.1):
        # define grid:
        self.xSize = int((width+cellSize/2)/cellSize) + 1
        self.ySize = int((height+cellSize/2)/cellSize) + 1
        self.grid = [[0 for x in range(self.ySize)] for x in range(self.xSize)]
        self.width = width
        self.height = height
        self.cellSize = float(cellSize)
        self.isDistanceGrid = False


    def _printGrid(self):
        print("xSize*ySize: ", self.xSize, self.ySize)
        for yi in range(self.ySize-1,-1,-1):
            s = ""
            for xi in range(self.xSize):
                s += "%1d" % self.grid[xi][yi]
            print(s)

    def drawGrid(self):
        # define graphic window:
        win = GraphWin("Occupancy Grid", int(800.0*self.width/self.height), 800, autoflush=False)
        win.setCoords(-self.cellSize, -self.cellSize, self.width+self.cellSize, self.height+2*self.cellSize)
        maxGridVal = max([max(l) for l in self.grid])

        # draw all grid cells:
        for yi in range(self.ySize):
            for xi in range(self.xSize):
                if not self.isDistanceGrid:
                    if self.grid[xi][yi] == 1:
                        p1 = Point(xi*self.cellSize, yi*self.cellSize)
                        p2 = Point((xi+1)*self.cellSize, (yi+1)*self.cellSize)
                        r = Rectangle(p1, p2)
                        r.setFill('black')
                        r.draw(win)
                else:
                    p1 = Point(xi * self.cellSize, yi * self.cellSize)
                    p2 = Point((xi + 1) * self.cellSize, (yi + 1) * self.cellSize)
                    r = Rectangle(p1, p2)
                    gray = int((self.grid[xi][yi]/maxGridVal)*255)
                    #print(self.grid[xi][yi],gray)
                    col = "#%02x%02x%02x" % (gray,gray,gray)
                    r.setFill(col)
                    r.setOutline(col)
                    r.draw(win)

        # close window when click:
        print("click in window to close")
        win.getMouse() # pause for click in window
        win.close()

    # --------
    # Add new a new line from point (x0,y0) to (x1,y1) to the occupancy grid.
    # Currently only horizontal or vertical lines ar allowed.
    # To Do: Implement Bresenham algorithm for arbitrary lines.
    #
    def _addLine(self, x0, y0, x1, y1, value = 1):
        if x0 != x1 and y0 != y1:
            raise ValueError('lines must be horizontal or vertical')
        x0_i = int(x0/self.cellSize + 0.5)
        y0_i = int(y0/self.cellSize + 0.5)
        # print x0, y0, x1, y1
        if x0 == x1:
            y1_i = int(y1/self.cellSize + 0.5)
            if y0_i < y1_i:
                for yi in range(y0_i,y1_i+1):
                    self.grid[x0_i][yi] = value
            else:
                for yi in range(y1_i,y0_i+1):
                    self.grid[x0_i][yi] = value
        else:
            x1_i = int(x1/self.cellSize + 0.5)
            if x0_i < x1_i:
                for xi in range(x0_i,x1_i+1):
                    self.grid[xi][y0_i] = value
            else:
                for xi in range(x1_i,x0_i+1):
                    self.grid[xi][y0_i] = value


    # --------
    # Set grid value at the coordinate (x,y).
    #
    def _setValue(self, x, y, value = 1):
        if x < 0 or x > self.width:
            return
        if y < 0 or y > self.height:
            return
        xi = int(x/self.cellSize + 0.5)
        yi = int(y/self.cellSize + 0.5)
        self.grid[xi][yi] = value


    # --------
    # Get grid value at the coordinate (x,y).
    #
    def getValue(self, x, y):
        if x < 0 or x > self.width:
            return
        if y < 0 or y > self.height:
            return
        xi = int(x/self.cellSize + 0.5)
        yi = int(y/self.cellSize + 0.5)
        return self.grid[xi][yi]


    def _extendToDistanceGrid(self):
        # openList is implemented as heap
        openList = [];
        # add all occupied grid cells in openList:
        for yi in range(self.ySize):
            for xi in range(self.xSize):
                if self.grid[xi][yi] == 1:
                    heapq.heappush(openList, (0,(xi,yi)))

        while len(openList) > 0:
            (_, val) = heapq.heappop(openList)
            (xi, yi) = val
            # jeden Nachbarn (xn,yn) von (xi,yi) betrachten:
            for xn in (xi-1,xi,xi+1):
                for yn in (yi-1,yi,yi+1):
                    if xn < 0 or xn >= self.xSize:
                        continue
                    if yn < 0 or yn >= self.ySize:
                        continue
                    dn = self.grid[xi][yi] + OccupancyGrid.__cost((xi, yi), (xn, yn)) * self.cellSize
                    if self.grid[xn][yn] == 0 or dn < self.grid[xn][yn]:
                        self.grid[xn][yn] = dn
                        heapq.heappush(openList, (dn, (xn, yn)))

        for yi in range(self.ySize):
            for xi in range(self.xSize):
                self.grid[xi][yi] -= 1

        self.isDistanceGrid = True
        return

    @staticmethod
    def __cost(v, w):
        (x1, y1) = v
        (x2, y2) = w
        if abs(x1-x2) == 1 and abs(y1-y2):
            return 1.41
        else:
            return 1.0


def _test1():
    myGrid = OccupancyGrid(0, 0, 0.8, 0.5)
    myGrid._setValue(0.0, 0.0)
    myGrid._setValue(0.1, 0.0)
    myGrid._setValue(0.3, 0.0)
    myGrid._setValue(0.4, 0.0)
    myGrid._setValue(0.5, 0.0)

    myGrid._setValue(0.0, 0.2)
    myGrid._setValue(0.1, 0.2)
    myGrid._setValue(0.3, 0.2)
    myGrid._setValue(0.4, 0.2)
    myGrid._setValue(0.5, 0.2)

    myGrid._setValue(0.8, 0.4)
    myGrid._setValue(0.8, 0.5)

    myGrid._extendToDistanceGrid()

    myGrid._printGrid()
    myGrid.drawGrid()

def _test2():
    myGrid = OccupancyGrid(0, 0, 0.8, 0.5)
    myGrid._addLine(0.1, 0.1, 0.7, 0.1)
    myGrid._addLine(0.7, 0.1, 0.7, 0.3)

    #myGrid.extendToDistanceGrid()
    myGrid._printGrid()
    myGrid.drawGrid()

if __name__ == "__main__":
    _test2()