"""
Author: Nicholas Nguyen
Final Project
File: room.py

Class for handling the dungeons the player walks around on
"""

from .vector2D import Vector2
from .drawable import Drawable
from .door import Door
from ..FSMs.gameObjectFSM import BasicState


class Room(Drawable):

    def __init__(self, imageName, roomNumber, connectingRoom=None,
                 north=False, east=False, south=False, west=False):
        super().__init__(imageName, Vector2(0, 0))
        # A list containing the 2 doors in the room
        self.doors = []

        # room ID number to allow for blitting of the right one
        self._roomNumber = roomNumber

        self._state = BasicState()

        # A list of the enemies in a specific room
        self.enemies = []

        # A list of the player arrows in fired in that room
        self.arrows = []

        self.upgrade = None
        self.stairs = None

        self._hasUpgrade = False
        self._upgradeGrabbed = False
        self._hasStairs = False

        # List holding all of the rocks in a room
        self.rocks = []

    def setNorthDoor(self, connectingRoom):
        self.doors.append(Door("North", connectingRoom))

    def setEastDoor(self, connectingRoom):
        self.doors.append(Door("East", connectingRoom))

    def setSouthDoor(self, connectingRoom):
        self.doors.append(Door("South", connectingRoom))

    def setWestDoor(self, connectingRoom):
        self.doors.append(Door("West", connectingRoom))

    def isClear(self):
        """Method to check if a room has no enemies"""
        return not bool(self.enemies)

    def getHasUpgrade(self):
        return self._hasUpgrade

    def setHasUpgrade(self, boolean):
        self._hasUpgrade = boolean

    def getHasStairs(self):
        return self._hasStairs

    def setHasStairs(self, boolean):
        self._hasStairs = boolean

    def getUpgradeGrabbed(self):
        return self._upgradeGrabbed

    def setUpgradeGrabbed(self, boolean):
        self._upgradeGrabbed = boolean

    def getRoomNumber(self):
        return self._roomNumber

    def __eq__(self, other):
        # https://www.pythontutorial.net/python-oop/python-__eq__/
        if isinstance(other, Room):
            return self._roomNumber == other._roomNumber
        else:
            return False

    def __str__(self):
        """Print out the room number so that the printed atlas looks good"""
        return str(self._roomNumber)

    def __lt__(self, other):
        if isinstance(other, Room):
            return self._roomNumber < other._roomNumber

    def __gt__(self, other):
        if isinstance(other, Room):
            return self._roomNumber > other._roomNumber
