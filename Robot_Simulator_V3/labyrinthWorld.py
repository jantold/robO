from Robot_Simulator_V3 import World

def buildWorld():
    world = World.World(20, 20)

    world.addLine( 1, 1,19, 1)
    world.addLine( 1, 1, 1,19)
    world.addLine( 7, 1, 7, 3)
    world.addLine(15, 1,15, 7)

    world.addLine( 3, 3, 3, 7)
    world.addLine( 5, 3, 5, 7)
    world.addLine( 5, 3, 7, 3)
    world.addLine( 9, 3, 9, 5)
    world.addLine(11, 3,13, 3)
    world.addLine(11, 3,11, 5)
    world.addLine(13, 3,13, 9)
    world.addLine(17, 3,17, 7)
    world.addLine(17, 3,19, 3)
    world.addLine(19, 3,19,19)

    world.addLine( 7, 5,11, 5)

    world.addLine( 3, 7,11, 7)
    world.addLine(11, 7,11,15)

    world.addLine( 3, 9, 3,11)
    world.addLine( 3, 9, 7, 9)
    world.addLine( 7, 9, 7,11)
    world.addLine( 9, 9, 9,13)
    world.addLine(13, 9,19, 9)

    world.addLine( 5,11, 5,15)
    world.addLine( 7,11, 9,11)
    world.addLine(13,11,17,11)
    world.addLine(17,11,17,17)

    world.addLine( 1,13, 5,13)
    world.addLine( 7,13, 9,13)
    world.addLine( 7,13, 7,15)
    world.addLine(15,13,15,19)

    world.addLine( 3,15, 5,15)
    world.addLine( 3,15, 3,17)
    world.addLine( 7,15, 9,15)
    world.addLine( 9,15, 9,17)
    world.addLine(11,15,13,15)

    world.addLine( 3,17, 7,17)
    world.addLine( 9,17,15,17)

    world.addLine( 1,19,19,19)

    return world