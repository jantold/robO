from Robot_Simulator_V3 import World

def buildWorld():
    world = World.World(18, 14)
    world.addLine( 2, 2, 16,  2)
    world.addLine(16, 2, 16, 12)
    world.addLine(16, 12, 4, 12)
    world.addLine( 4, 12, 4, 10)
    world.addLine( 4, 10, 2, 10)
    world.addLine( 2, 10, 2,  2)

    return world