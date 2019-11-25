from Robot_Simulator_V3 import World

def buildWorld():
    world = World.World(25, 10)

    world.addLine(9, 4, 10, 4)
    world.addLine(10, 4, 10, 6)
    world.addLine(10, 6, 9, 6)
    world.addLine(9, 6, 9, 4)

    world.addLine(13, 5, 14, 5)
    world.addLine(14, 5, 14, 7)
    world.addLine(14, 7, 13, 7)
    world.addLine(13, 7, 13, 5)

    #polyline = [[5,5.5],[15,5.5]]

    return world