from Robot_Simulator_V3 import World

def buildWorld():
    world = World.World(20, 10)

    world.addLine(1, 5, 10, 5)
    world.addLine(11, 5, 19, 5)
    world.addLine(1, 7, 19, 7)

    # world.addLine(5, 5.3, 5, 6)
    # world.addLine(5, 6, 5.5, 6)
    # world.addLine(5.5, 6, 5.5, 5.3)
    # world.addLine(5, 5.3, 5.5, 5.3)

    world.addBox(13, 6)
    world.addBox(10.5,3)

    #polyline = [[1,6],[10.5,6],[10.5,3]]
    #world.drawPolyline(polyline)

    return world