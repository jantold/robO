from Robot_Simulator_V3 import World

def buildWorld():
    world = World.World(20, 10)

    world.addLine(1, 5, 10, 5)
    world.addLine(11, 5, 19, 5)

    world.addLine(1, 7, 19, 7)

    world.addLine(11, 5, 11, 3.5)
    world.addLine(11, 2.5, 11, 1)

    world.addBox(15,3)

    polyline = [[1,6],[10.5,6],[10.5,3],[15,3]]
    world.drawPolyline(polyline)

    return world