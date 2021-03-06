"""
Author: Nicholas Nguyen
Final Project
File: arrow.py

Class for the player's projectiles
"""

import pygame
from .projectile import Projectile

BASE_DAMAGE = 5
BASE_VSPEED = 250


class Arrow(Projectile):

    damageLevel = 0
    speedLevel = 0

    @classmethod
    def iterateDamageLevel(cls):
        cls.damageLevel += 1

    @classmethod
    def iterateSpeedLevel(cls):
        cls.speedLevel += 1

    def __init__(self, initialPosition):
        actualDamage = BASE_DAMAGE + self.damageLevel
        super().__init__("arrow.png", initialPosition, actualDamage)

        # 0 means horizontal, 1 means vertical
        self._direction = 0

        # Variable used to track direction arrows fly
        self._posOrNeg = 1

        self._vspeed = BASE_VSPEED

    def changeDirection(self, event):
        """Function to change if the arrow is vertical or
           horizontal based on the arrow key inputted"""
        if event.key == pygame.K_DOWN:
            self._direction = 1
            self._posOrNeg = 1

        elif event.key == pygame.K_UP:
            self._direction = 1
            self._posOrNeg = -1

        if event.key == pygame.K_LEFT:
            self._direction = 0
            self._posOrNeg = -1

        if event.key == pygame.K_RIGHT:
            self._direction = 0
            self._posOrNeg = 1

    def draw(self, surface, offset):
        # Shooting down
        if self._direction == 1 and self._posOrNeg == 1:
            # Start it on the archer
            surface.blit(self._image, list(self._position - offset))

        # Shooting up
        elif self._direction == 1 and self._posOrNeg == -1:
            surface.blit(pygame.transform.rotate(self._image, 180),
                         list(self._position - offset))
        # Shooting left
        elif self._direction == 0 and self._posOrNeg == -1:
            surface.blit(pygame.transform.rotate(self._image, 270),
                         list(self._position - offset))

        # Shooting right
        elif self._direction == 0 and self._posOrNeg == 1:
            surface.blit(pygame.transform.rotate(self._image, 90),
                         list(self._position - offset))

    def update(self, seconds):
        # Update the position based on the velocity and direction
        self._position[self._direction] += self._vspeed *\
                                           self._posOrNeg * seconds
