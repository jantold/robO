from Robot_Simulator_V3 import World

def buildWorld():
    world = World.World(40, 20)

    #polyline = [[5,4],[5,16]]

    world.addLine(4, 15, 4, 5)
    world.addLine(6, 15, 6, 5)

    world.addLine(4, 10, 5, 10)
    world.addLine(4, 9, 5, 9)
    world.addLine(5, 9, 5, 10)

    #world.addLine(1, 5, 10, 5)
    return world