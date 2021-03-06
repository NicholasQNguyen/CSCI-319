import pygame
import os
from ..gameObjects.drawable import Drawable


class AbstractUIEntry(Drawable):
    """ Basic UI Entry Class
    Sets parallax to zero and contains information about fonts"""

    if not pygame.font.get_init():
        pygame.font.init()

    _FONT_FOLDER = os.path.join("resources", "fonts")
    _DEFAULT_FONT = "PressStart2P.ttf"
    _DEFAULT_SIZE = 32

    FONTS = {
        "default": pygame.font.Font(os.path.join(
                                    _FONT_FOLDER, _DEFAULT_FONT),
                                    _DEFAULT_SIZE),
        "default8": pygame.font.Font(os.path.join(
                                     _FONT_FOLDER, _DEFAULT_FONT), 8),
        "default16": pygame.font.Font(os.path.join(
                                     _FONT_FOLDER, _DEFAULT_FONT), 16),
        "default32": pygame.font.Font(os.path.join(
                                      _FONT_FOLDER, _DEFAULT_FONT), 32)
    }

    def __init__(self, position):
        super().__init__("", position)


class Text(AbstractUIEntry):
    """A plain text UI entry."""

    def __init__(self, position, text, font="default", color=(255, 255, 255)):
        super().__init__(position)
        self._color = color

        self._font = font

        self._image = AbstractUIEntry.FONTS[self._font].render(
                                                  text, False, self._color)

    def setText(self, newText):
        self._image = AbstractUIEntry.FONTS[self._font].render(
                                                  newText, False, self._color)
