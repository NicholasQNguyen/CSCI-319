"""
Author: Nicholas Nguyen
Final Porject
File: squads.py


A class to hold onto and manage groups of enemies
"""
from random import randint
from .slime import Slime
from .golem import Golem
from .tower import Tower
from .dragon import Dragon
from .vector2D import Vector2


GOLEM_VELOCITY = 2


class Squads(object):

    @classmethod
    def slimeOverload(cls):
        slimeOverloadList = []
        for i in range(10):
            # Spawn 10 slimes in the top left of the map
            slimeOverloadList.append(Slime(Vector2(randint(0, 504),
                                                   randint(0, 504))))
        return slimeOverloadList

    @classmethod
    def golemAttack(cls):
        golemAttackList = []
        for i in range(3):
            golemAttackList.append(Golem(Vector2(randint(500, 808),
                                                 randint(0, 508))))
        return golemAttackList

    @classmethod
    def golemAndSlimeOhNo(cls):
        golemAndSlimeOhNoList = []
        golemAndSlimeOhNoList.append(Golem(Vector2(randint(500, 808),
                                                   randint(0, 508))))
        for i in range(5):
            golemAndSlimeOhNoList.append(Slime(Vector2(randint(0, 504),
                                                       randint(0, 504))))
        return golemAndSlimeOhNoList

    @classmethod
    def dodgeThis(cls):
        dodgeThisList = []
        for i in range(5):
            dodgeThisList.append(Tower(Vector2(randint(0, 800),
                                               randint(0, 504))))
        return dodgeThisList

    @classmethod
    def theChase(cls):
        theChaseList = []
        theChaseList.append(Golem(Vector2(randint(500, 808),
                                          randint(0, 508))))
        for i in range(3):
            theChaseList.append(Tower(Vector2(randint(0, 800),
                                               randint(0, 504))))
        return theChaseList

    @classmethod
    def shooterAndBodyguards(cls):
        shooterAndBodyguardsList = []
        for i in range(3):
            shooterAndBodyguardsList.append(Tower(Vector2(randint(0, 800),
                                                          randint(0, 504))))
        for i in range(5):
            shooterAndBodyguardsList.append(Slime(Vector2(randint(0, 504),
                                                          randint(0, 504))))
        return shooterAndBodyguardsList


    @classmethod
    def dragon(cls):
        return [Dragon(Vector2(randint(200, 808),
                               randint(0, 500)))]
