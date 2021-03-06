from .basicManager import BasicManager
from .gameManager import GameManager
from ..FSMs.screenFSM import ScreenState
from ..UI.items import Text
from ..UI.displays import *
from ..gameObjects.vector2D import Vector2
from ..UI.screenInfo import SCREEN_SIZE
import pygame

class ScreenManager(BasicManager):
      
   def __init__(self):
      super().__init__()
      self._game = GameManager(SCREEN_SIZE)
      self._state = ScreenState()
      self._pausedText = Text(Vector2(0,0),"Paused")
      
      size = self._pausedText.getSize()
      midPointX = SCREEN_SIZE.x // 2 - size[0] // 2
      midPointY = SCREEN_SIZE.y // 2 - size[1] // 2
      
      self._pausedText.setPosition(Vector2(midPointX, midPointY))
      
      self._mainMenu = EventMenu("background.png", fontName="default8")
      self._mainMenu.addOption("start", "Press 1 to Start Game",
                               SCREEN_SIZE // 2 - Vector2(0,50),
                               lambda x: x.type == pygame.KEYDOWN and x.key == pygame.K_1,
                               center="both")
      self._mainMenu.addOption("exit", "Press 2 to Exit Game",
                               SCREEN_SIZE // 2 + Vector2(0,50),
                               lambda x: x.type == pygame.KEYDOWN and x.key == pygame.K_2,
                               center="both")
   
   
   def draw(self, drawSurf):
      if self._state == "game":
         self._game.draw(drawSurf)
      
         if self._state.isPaused():
            self._pausedText.draw(drawSurf)
      
      elif self._state == "mainMenu":
         self._mainMenu.draw(drawSurf)
   
   def handleEvent(self, event):
      # Handle screen-changing events first
      if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
         self._state.manageState("pause", self)
      elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:
         self._state.manageState("mainMenu", self)
      else:
         if self._state == "game" and not self._state.isPaused():
            self._game.handleEvent(event)
         elif self._state == "mainMenu":
            choice = self._mainMenu.handleEvent(event)
            
            if choice == "start":
               self._state.manageState("startGame", self)
            elif choice == "exit":
               return "exit"
   
   
   def update(self, ticks):      
      if self._state == "game" and not self._state.isPaused():
         self._game.update(ticks, SCREEN_SIZE)
      elif self._state == "mainMenu":
         self._mainMenu.update(ticks)
   
   
   # Prevents kirby from constantly walking if the direction arrow
   #  is released when the game isn't playing
   def transitionState(self, state):
      if state == "game" and not self._state.isPaused():
         self._game.updateMovement()
