"""
Author: Nicholas Nguyen
Final Project
File: golem.py

Monster that follows the player
"""
from .alive import Alive
from ..FSMs.gameObjectFSM import GolemState
# from ..managers.frameManager import FrameManager

GOLEM_HP = 20
GOLEM_V_SPEED = 100
GOLEM_DAMAGE = 5


class Golem(Alive):

    def __init__(self, position):
        super().__init__("golem-walk.png", position, GOLEM_HP)

        self._vspeed = GOLEM_V_SPEED

        self._nFramesList = {
            "up": 5,
            "left": 5,
            "down": 5,
            "right": 5,
            "standing": 5}

        self._rowList = {
             "up": 0,
             "left": 1,
             "down": 2,
             "right": 3,
             "standing": 0}

        self._framesPerSecondList = {
            "up": 10,
            "left": 10,
            "down": 10,
            "right": 10,
            "standing": 10}

        self._state = GolemState()

        self._damage = GOLEM_DAMAGE

    def whereIsTheArcherX(self, archerPosition):
        if archerPosition[0] > self._position[0]:
            return "right"
        elif archerPosition[0] < self._position[0]:
            return "left"

    def whereIsTheArcherY(self, archerPosition):
        if archerPosition[1] > self._position[1]:
            return "down"
        elif archerPosition[1] < self._position[1]:
            return "up"

    def changeDirection(self, archerPosition, stopAll=False):
        actionX = self.whereIsTheArcherX(archerPosition)
        actionY = self.whereIsTheArcherY(archerPosition)
        self._state.manageState(actionX, actionY, self, stopAll)
