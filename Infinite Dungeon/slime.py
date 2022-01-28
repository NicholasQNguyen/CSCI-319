"""
Author: Nicholas Nguyen
Project 2
File: target.py

Basic monster that moves back and forth.
"""
import pygame
from alive import Alive
import os


class Slime(Alive):

    def __init__(self, position, velocity):
        super().__init__(position, velocity, "slime_monster_spritesheet.png")
        tempSurface = pygame.Surface((24, 24))
        tempSurface.blit(self._image, (0, 0))
        self._image = tempSurface
        self._direction = 1

    def changeDirection(self):
        self._direction *= -1

    def move(self, seconds):
        """Move right for 5 seconds then left for 5 seconds"""
        self._position[0] += self._velocity * self._direction