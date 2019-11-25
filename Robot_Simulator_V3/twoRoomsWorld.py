from Robot_Simulator_V3 import World

def buildWorld():
    world = World.World(18, 14)
    world.addLine(1, 1, 15, 1)
    world.addLine(15, 1, 15, 9)
    world.addLine(15, 10.5, 15, 13)
    world.addLine(15, 13, 1, 13)
    world.addLine(1, 13, 1, 1)

    # room 1 and 2
    world.defineRoom('Room 01', 4, 1.5)
    world.defineRoom('Room 02', 11, 1.5)
    world.addLine(8, 1, 8, 2)
    world.addLine(8, 3.5, 8, 13)

    # depot
    world.defineRoom('depot', 16, 12.5)
    world.addLine(15, 13, 17, 13)
    world.addLine(17, 13, 17, 12)

    # Boxes:
    world.addBox(3.2,  1.5)
    world.addBox(2.0, 11.5)
    world.addBox(7.2,  9.8)

    world.addBox(8.7, 12.2)
    world.addBox(13.5, 2.0)
    return world