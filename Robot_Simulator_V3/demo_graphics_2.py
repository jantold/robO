# Bewegung von 100 Partikeln testen.
# O. Bittel; 13.09.2018

from Robot_Simulator_V3.graphics import *
import random

def main():
    win = GraphWin("My Animation", 1200, 1200, autoflush=False)
    win.setBackground('lightgrey')
    win.setCoords(0, 0, 1200, 1200)

    cl = []
    for i in range(1,100):
        x = random.randint(400,500)
        y = random.randint(400,500)
        c = Circle(Point(x,y), 5)
        c.draw(win)
        cl.append(c)
    win.update()
    win.getMouse() # pause for click in window

    for i in range(5):
        for c in cl:
            c.move(100,100)
        win.update()
        win.getMouse() # pause for click in window

    win.close()

main()