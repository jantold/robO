# Kreis bewegen mit Maus
# O. Bittel; 13.09.2018

from Robot_Simulator_V3.graphics import *
import random

def main():
    win = GraphWin("My Circle", 500, 500)
    win.setBackground('blue')
    c = Circle(Point(250,250), 10)
    c.setFill('red')
    c.draw(win)
    win.getMouse() # pause for click in window

    for i in range(1,10):
        win.getMouse() # pause for click in window
        dx = random.randint(-20,20)
        dy = random.randint(-20,20)
        if i%2 == 0:
            c.setFill('green')
        else:
            c.setFill('white')
        c.move(dx,dy)

    win.close()

main()