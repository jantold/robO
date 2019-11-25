# Kreis und Line zeichnen
# O. Bittel; 13.09.2018

from Robot_Simulator_V3.graphics import *

def main():
    win = GraphWin("My Circle", 500, 500) # Fenstergroesse 500*500 Pixel
    win.setCoords(0,0,5,5) # Linker unterer Punkt ist (0,0) und rechter oberer Punkt ist (5,5)
    win.setBackground('lightgrey')

    # draw Ploygon:
    poly = Polygon(Point(0.1,0.1), Point(4,0.1), Point(2,4.9))
    poly.setFill('green')
    poly.draw(win)

    # draw circle:
    c = Circle(Point(2.5, 2.5), 0.3)
    c.setFill('red')
    c.draw(win)

    # draw line:
    l = Line(Point(1.0, 0.5), Point(4.0, 2.5))
    l.setFill('blue')
    l.draw(win)

    win.getMouse() # pause for click in window
    win.close()

main()