from Robot_Simulator_V3 import World

def buildWorld():
    world = World.World(40, 20)

    world.addLine(10, 4, 11, 4)
    world.addLine(11, 4, 11, 6)
    world.addLine(11, 6, 10, 6)
    world.addLine(10, 6, 10, 4)

    world.addLine(13,10,15,10)
    world.addLine(16,10,18,10)

    world.addLine(13,12,14,12)
    world.addLine(15,12,18,12)


    #polyline = [[5,5],[15,5],[15,15],[5,15],[5,5]]

    world.addLine(4, 15, 4, 5)
    world.addLine(6, 15, 6, 5)

    world.addLine(4, 10, 5, 10)
    world.addLine(4, 9, 5, 9)
    world.addLine(5, 9, 5, 10)

    #world.addLine(1, 5, 10, 5)
    return world