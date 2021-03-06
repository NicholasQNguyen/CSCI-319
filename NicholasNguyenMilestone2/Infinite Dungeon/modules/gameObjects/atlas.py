"""
Author: Nicholas Nguyen
Final Porject
File: atlas.py


A class to hold onto and manage rooms
"""

from random import randint, choice
from .room import Room
from .squads import Squads
from .upgrade import DamageUpgrade, SpeedUpgrade, ProjectileSpeedUpgrade
from .stairs import Stairs
from .rock import Rock
from .vector2D import Vector2

DIMENSION = 4
ROOM_TYPES = ["basicRoom.png", "bridgeRoom.png", "torchRoom.png"]


class Atlas(object):

    def __init__(self):
        # Initialize the enemy squad types
        squads = [Squads.slimeOverload,
                  Squads.golemAttack,
                  Squads.golemAndSlimeOhNo]

        # Initialize the upgrades
        upgrades = [DamageUpgrade,
                    SpeedUpgrade,
                    ProjectileSpeedUpgrade]

        self.atlas = []
        self.listOfRooms = []
        # Make a DIMENSIONxDIMENSION grid to represent the map
        for i in range(DIMENSION):
            self.atlas.append([])
            for j in range(DIMENSION):
                self.atlas[i].append(0)

        prevRoom = 0
        roomAssignment = 1
        nextRoom = 2

        up = False

        placerIndex1 = DIMENSION - 1
        placerIndex2 = 0

        firstRoom = Room("firstRoom.png", 0, 1)
        lastRoom = Room(choice(ROOM_TYPES), 99)

        # Put a room in the bottom left and top right of the grid
        self.atlas[placerIndex1][placerIndex2] = firstRoom
        self.atlas[placerIndex2][placerIndex1] = lastRoom

        # Keep adding rooms until we see the last room
        while isinstance(self.getNorth((placerIndex1,
                                        placerIndex2)),
                         int) and\
            isinstance(self.getEast((placerIndex1,
                                     placerIndex2)),
                       int):
            # From the bottom left room, go randomly
            # right or up and put a room
            rightOrUp = randint(0, 1)
            if rightOrUp == 0:
                up = True

            if up:
                placerIndex1 -= 1
                # Account for if we're on the top edge of the map
                if placerIndex1 != 0:
                    newRoom = Room(choice(ROOM_TYPES), roomAssignment,
                                   prevRoom, nextRoom)
                    newRoom.setSouthDoor((prevRoom))
                    self.atlas[placerIndex1][placerIndex2] = newRoom
                    up = False
                    # Go to the previous room and add a door
                    # to link to the new room we just made
                    self.atlas[placerIndex1 + 1][placerIndex2] \
                        .setNorthDoor(roomAssignment)
                # If we just get a bunch of up, then go right
                else:
                    up = False
                    placerIndex1 += 1
                    placerIndex2 += 1
                    newRoom = Room(choice(ROOM_TYPES), roomAssignment,
                                   prevRoom, nextRoom)
                    newRoom.setWestDoor(prevRoom)
                    self.atlas[placerIndex1][placerIndex2] = newRoom
                    # In the previous room, add a door
                    # to the east to match up with this room
                    self.atlas[placerIndex1][placerIndex2 - 1]\
                        .setEastDoor(roomAssignment)

            else:
                placerIndex2 += 1
                # If we're on the right edge of the map
                try:
                    newRoom = Room(choice(ROOM_TYPES), roomAssignment,
                                   prevRoom, nextRoom)
                    newRoom.setWestDoor(prevRoom)
                    self.atlas[placerIndex1][placerIndex2] = newRoom
                    # In the previous room, add a door
                    # to the east to match up with this room
                    self.atlas[placerIndex1][placerIndex2 - 1]\
                        .setEastDoor(roomAssignment)
                except IndexError:
                    placerIndex2 -= 1
                    placerIndex1 -= 1
                    newRoom = Room(choice(ROOM_TYPES), roomAssignment,
                                   prevRoom, nextRoom)
                    newRoom.setSouthDoor(prevRoom)
                    self.atlas[placerIndex1][placerIndex2] = newRoom
                    # Go to the previous room and add a door
                    # to link to the new room we just made
                    self.atlas[placerIndex1 + 1][placerIndex2]\
                        .setNorthDoor(roomAssignment)

            roomAssignment += 1
            prevRoom += 1
            nextRoom += 1

        # if we're one below the final room, add a door pointing up
        if self.getNorth((placerIndex1, placerIndex2)) == lastRoom:
            self.atlas[placerIndex1][placerIndex2].setNorthDoor(99)
            # add a door pointing back to the second to last room
            lastRoom.setSouthDoor(prevRoom)

        # If we're one to the left of the final room,
        # add a door pointing right
        elif self.getEast((placerIndex1, placerIndex2)) == lastRoom:
            self.atlas[placerIndex1][placerIndex2].setEastDoor(99)
            lastRoom.setSouthDoor(prevRoom)

        # a list of the rooms
        for i in range(DIMENSION):
            for j in range(DIMENSION):
                if self.atlas[i][j] != 0:
                    self.listOfRooms.append(self.atlas[i][j])

        # We want a sorted list so that when we index in main,
        # we get the right room
        self.listOfRooms.sort()

        # Assign an enemy squad to each room
        for room in self.listOfRooms:
            # Don't assign to the first room
            if room.getRoomNumber() == 0:
                pass
            else:
                room.enemies = choice(squads)()

        # Assign an upgrade to each room besides the first and last room
        for room in self.listOfRooms:
            if room.getRoomNumber() != 0 or room.getRoomNumber() != 99:
                room.upgrade = choice(upgrades)()

        # Place a random number of rocks in each room
        for room in self.listOfRooms:
            if room.getRoomNumber() != 0:
                for i in range(randint(0, 10)):
                    room.rocks.append(Rock(Vector2(randint(200, 808),
                                                   randint(200, 808))))

        # Assign a stair to the last room
        self.listOfRooms[-1].stairs = Stairs()

    def getRooms(self):
        """Get a list of the rooms in order.
        IE. [Room 0, Room 1, Room 2 etc.]"""
        return self.listOfRooms

    def hasNorth(self, indeces):
        try:
            return bool(self.atlas[indeces[0]-1][indeces[1]])
        except IndexError:
            return None

    def hasEast(self, indeces):
        try:
            return bool(self.atlas[indeces[0]][indeces[1]+1])
        except IndexError:
            return None

    def hasWest(self, indeces):
        try:
            return bool(self.atlas[indeces[0]][indeces[1]-1])
        except IndexError:
            return False

    def hasSouth(self, indeces):
        try:
            return bool(self.atlas[indeces[0]+1][indeces[1]])
        except IndexError:
            return False

    def getNorth(self, indeces):
        try:
            return self.atlas[indeces[0]-1][indeces[1]]
        except IndexError:
            return False

    def getEast(self, indeces):
        try:
            return self.atlas[indeces[0]][indeces[1] + 1]
        except IndexError:
            return False

    def __str__(self):
        # https://stackoverflow.com/questions/50731788/str-to-give-a-visual-representation-of-the-2d-table-in-python
        return ('\n'.join(['|'.join([str(cell) for cell in row])
                for row in self.atlas]))


"""
            The map looks like this:
            [0, 0, 0]
            [0, 0, 0]
            [0, 0, 0]
"""
