HTWG_Robot_Simulator_AIN_V2.0
25.09.2019
Oliver Bittel
Fakultät Informatik


Umgebung:
=========
Module wurden mit Python 3.5 getestet und
der Entwicklungsumgebung PyCharm Community Edition 2018.2


Installierte Pakete:
numpy (zum Rechnen mit Vekoren und Matrizen)
matplotlib (nützlich, falls Graphiken geplottet werden sollen; ähnlich wie plot von matlab)


Benutzung:
==========
1. demo_xxx:
demo_xxx sind kleine Hauptprogramme, die vorhandene Klassen testen.


2. graphics.py:
graphics.py ist ein kleines Paket zum Zeichnen von Graphikobjekten.
Dokumentation siehe graphics.pdf.
Das Paket stammt von http://mcsp.wartburg.edu/zelle/python/


3. Robot.py und World.py:
Diese beiden Klassen bilden den eigentlichen Simulator.
Eine Simulation besteht aus genau einem Objekt myRobot der Klasse Robot und einem
Objekt myWorld der Klasse World.
myRobot wird in der Welt myWorld mit dem Aufruf

    myWorld.setRobot(myRobot,[x,y,theta])

positioniert. Der Roboter lässt sich über

    myRobot.move()

steuern. Sensordaten können über

    myRobot.sense() bzw.
    myRobot.senseBoxes()

abgefragt werden. Siehe demo_Simulator_1.py.

Für Pick-And-Place-Aufgaben stehen die Methoden

    pickUpBox, placeBox und boxInPickUpPosition.

zur Verfügung. Wichtig: Eine Box darf nur aufgenommen werden, wenn sie im
Pick-Up-Bereich des Roboters liegt (siehe Instanzvariablen in der Klasse Robot)
und der Roboter aktuell keine Box aufgenommen hat. Siehe demo_Simulator_6.py.


4. KeyboradController.py:
Der Roboter kann manuell (zu Demozwecken) über die Cursortasten gesteuert werden.
Siehe demo_Simulator_2.py.
Boxen können über 'd' (down) und 'u' (up) aufgenommen bzw. abgelegt werden.
Siehe demo_Simulator_3.py.


5. xxxWorld.py
Verschiedene bereits vordefinierte Welten.


6. OccupancyGrid.py:
Klasse für Belegtheitsgitter.
Mit der Methode World.getOccupancyGrid() kann aus den
Weltdaten ein Belegtheitsgitter erzeugt werden.
Mit der Methode World.extendToDistanceGrid() kann ein
Belegtheitsgitter zu einem Distanzgitter erweitert werden.
Siehe demo_Simulator_4.py.


7. sensorUtilities
Enthält Funktionen um aus Sensordaten in Polarkoordinaten
einen Liste von Liniensegmente zu extrahieren.
Siehe demo_Simulator_5.py.


8. geometry
Enthält Funktionen zur Berechnung von geometrischen Aufgabenstellungen in 2D
wie Abstand Punkt-Punkt, Punkt-Gerade, Punkt-Segment und
Schnittpunkte von Geraden, Segmenten und Strahlen, u.a


Namenskonventionen:
===================

Xyz.py  Datei mit Definition der Klasse Xyz
xyz.py  Python-Skript oder Datei mit Funktionen (Funktionsmodul)

f()     Öffentliche Methode oder Funktion (public)
_f()    Methode oder Funktion nur für den internen Gebrauch (package access)
__f()   private Methode oder Funktion

_xyz    Instanzvariable nur für den internen Gebrauch (package access)
__xyz   private Instanzvariable