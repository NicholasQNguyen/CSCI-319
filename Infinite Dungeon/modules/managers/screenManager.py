from .gameManager import GameManager
from .basicManager import BasicManager
from .inputManager import InputManager
from .highScoreFunctions import checkIfHighScore, getHighScores
from .highScoreManager import HighScoreManager

from ..FSMs.screenFSM import ScreenState
from ..UI.items import Text
from ..UI.displays import CursorMenu
from ..gameObjects.vector2D import Vector2
from ..UI.screenInfo import SCREEN_SIZE

import pygame


class ScreenManager(BasicManager):

    def __init__(self):
        super().__init__()
        # Read the high score csv
        self._highScores = getHighScores()

        self._highScoreManager = HighScoreManager(SCREEN_SIZE, self._highScores)

        self._state = ScreenState()
        self._pausedText = Text(Vector2(0, 0), "Paused", "default16")

        size = self._pausedText.getSize()
        midPointX = SCREEN_SIZE.x // 2 - size[0] // 2
        midPointY = SCREEN_SIZE.y // 2 - size[1] // 2

        self._pausedText.setPosition(Vector2(midPointX, midPointY))

        self._mainMenu = CursorMenu("title.png", fontName="default32")
        self._mainMenu.addOption("start", "Start Game",
                                 SCREEN_SIZE // 2 - Vector2(0, 50),
                                 center="both")
        self._mainMenu.addOption("exit", "Exit Game",
                                 SCREEN_SIZE // 2 + Vector2(0, 50),
                                 center="both")
        self._mainMenu.addOption("highScore", "High Scores",
                                 SCREEN_SIZE // 2 + Vector2(0, 150),
                                 center="both")

        self._gameOver = CursorMenu("gameOver.png", fontName="default32")
        self._gameOver.addOption("exit", "Exit Game",
                                 SCREEN_SIZE // 2 - Vector2(0, 50),
                                 center="both")

    def draw(self, drawSurf):
        if self._state == "game":
            self._game.draw(drawSurf)

            if self._state.isPaused():
                self._pausedText.draw(drawSurf)

        elif self._state == "mainMenu":
            self._mainMenu.draw(drawSurf)

        elif self._state == "gameOver":
            self._gameOver.draw(drawSurf)

        elif self._state == "nameInput":
            self._nameInput.draw(drawSurf)

        elif self._state == "highScore":
            self._highScoreManager.draw(drawSurf)

    def handleEvent(self, event):
        # Handle screen-changing events first
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p and self._state == "game":
            self._state.manageState("pause", self)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_m and self._state == "game":
            self._state.manageState("mainMenu", self)
        else:
            if self._state == "game" and not self._state.isPaused():
                self._game.handleEvent(event)

            elif self._state == "mainMenu":
                choice = self._mainMenu.handleEvent(event)

                if choice == "start":
                    self._game = GameManager(SCREEN_SIZE)
                    self._state.manageState("startGame", self)
                elif choice == "exit":
                    return "exit"
                elif choice == "highScore":
                    self._state.manageState("highScore", self)

            elif self._state == "gameOver":
                choice = self._gameOver.handleEvent(event)

                if choice == "exit":
                    return "exit"

            elif self._state == "nameInput":
                choice = self._nameInput.handleEvent(event)
                if choice[0] == "submit":
                    # Make a highScoreManager with the high scores and the name inputted
                    self._highScoreManager = HighScoreManager(SCREEN_SIZE, self._highScores, choice[1])
                    self._state.manageState("highScore", self)

            elif self._state == "highScore":
                choice = self._highScoreManager.handleEvent(event)
                if choice == "mainMenu":
                    self._state.manageState("mainMenu", self)

    def update(self, ticks):
        if self._state == "game" and not self._state.isPaused():
            status = self._game.update(ticks, SCREEN_SIZE)
            if status[0] == "dead":
                # See if the player got a new high score
                self._highScores = checkIfHighScore(self._highScores, status[1])
                # If they did, then go to name input screen
                if self._highScores != False:
                    # Make the name input screen with the new high score
                    self._nameInput = InputManager(SCREEN_SIZE, status[1])
                    self._state.manageState("nameInput", self)
                # else just go to normal game over screen
                else:
                    status = None
                    self._state.manageState("gameOver", self)

        elif self._state == "mainMenu":
            self._mainMenu.update(ticks)

        elif self._state == "gameOver":
            self._gameOver.update(ticks)

        elif self._state == "nameInput":
            self._nameInput.update()

        elif self._state == "highScore":
            self._highScoreManager.update()

    # Prevents kirby from constantly walking if the direction arrow
    #  is released when the game isn't playing
    def transitionState(self, state):
        if state == "game" and not self._state.isPaused():
            self._game.updateMovement()
