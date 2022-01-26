"""
Author: Nicholas Nguyen
Project 2
File: target.py

Test target for collision testing.
"""

from drawable import Drawable
from vector2D import Vector2
import pygame
import os


class Target(Drawable):

    def __init__(self, position):
        super().__init__("rangeSmaller.png")
        sprite = pygame.image.load(os.path.join("images", "rangeSmaller.png")).convert_alpha()
        self._image = pygame.Surface((16, 16))
        self._image.blit(sprite, (0, 0))
   
        self._position = position 
