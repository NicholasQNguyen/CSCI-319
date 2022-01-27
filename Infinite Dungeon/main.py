"""
Author: Nicholas Nguyen
Infinite Dungeon
File: main.py
"""

import pygame
import os
from vector2D import Vector2
from archer import Archer
from arrow import Arrow
from copy import deepcopy
from target import Target
from random import randint
from drawable import Drawable
from slime import Slime


WORLD_SIZE = Vector2(1200, 1200)
SCREEN_SIZE = Vector2(800, 800)
SCALE_FACTOR = 1 
UPSCALED = SCREEN_SIZE * SCALE_FACTOR
BEGINNING = Vector2(-600, -600)
ARROW_KEYS = [pygame.K_DOWN, pygame.K_UP,
              pygame.K_LEFT, pygame.K_RIGHT]
WASD_KEYS = [ord("s"), ord("w"), ord("a"), ord("d")]


def main():
    # Initialize the module
    pygame.init()

    # Get the screen
    screen = pygame.display.set_mode(list(UPSCALED))

    # background background
#     background = Drawable("water1.png", Vector2(0, 0))

    # Let's make a background so we can see if we're moving
    dungeonFloor = Drawable("basicDungeonCropped.png", Vector2(0, 0))
    drawSurface = pygame.Surface(list(SCREEN_SIZE))

    # Stuff for the hero character
    archer = Archer((Vector2(500, 500)), 4, "archer.png")

    # List of arrows to keep track of them
    arrows = []

    # List of the targets
    targets = []
    # put 5 targets in 5 random positions
    for i in range(5):
        targets.append(Target(Vector2(randint(0, 1200), randint(0, 1200))))

    # List for the slimes
    slimes = []
    for i in range(3):
        slimes.append(Slime(Vector2(randint(300, 600), randint(300, 600)), 2))

    offset = Vector2(0, 0)

    gameClock = pygame.time.Clock()
    seconds = 0

    pygame.time.set_timer(pygame.USEREVENT, 5000)

    RUNNING = True

    while RUNNING:

        # Blit the background
#         background.draw(drawSurface, offset)
        drawSurface.fill((255, 255, 255))
    
        # Blit the dungeon floor
        dungeonFloor.draw(drawSurface, offset)

        archer.draw(drawSurface, offset)

        for arrow in arrows:
            arrow.draw(drawSurface, offset)

        for target in targets:
            target.draw(drawSurface, offset)

        for slime in slimes:
            slime.draw(drawSurface, offset)

        pygame.transform.scale(drawSurface, list(UPSCALED), screen)

        pygame.display.flip()

        # event handling, gets all event from the eventqueue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT or \
               (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                # change the value to False, to exit the main loop
                RUNNING = False

            elif event.type == pygame.KEYDOWN:
                # If the key in an arrow, apply it to the player's arrows 
                if event.key in ARROW_KEYS:
                    arrow = Arrow(deepcopy(archer.getPosition()), 5, "arrow.png")
                    # Set the direction based on what arrow was hit
                    arrow.changeDirection(event)
                    arrows.append(arrow)

                elif event.key in WASD_KEYS:
                    archer.handleEvent(event)

            elif event.type == pygame.KEYUP:

                if event.key in WASD_KEYS:
                    archer.handleEvent(event)

            elif event.type == pygame.USEREVENT:
                for slime in slimes:
                    slime.changeDirection()

        gameClock.tick(60)
        # seconds = gameClock.get_time() / 1000
        seconds = pygame.time.get_ticks() / 1000

    
        # Stuff for object movement

        for arrow in arrows:
            arrow.update()
            arrowCollisionRect = arrow.getCollideRect()

        for slime in slimes:
            slime.move(seconds)

        archer.update()

        # Check if arrows are beyond the border and delete them if they are
        for arrow in arrows:
            if arrow.getX() > WORLD_SIZE[0] or arrow.getX() < 0 or \
               arrow.getY() > WORLD_SIZE[1] or arrow.getY() < 0:
                arrow.isDead()

        # Collision Checking
        for target in targets:
            targetCollisionRect = target.getCollideRect()
            if arrows != []:
                if targetCollisionRect.colliderect(arrowCollisionRect):
                    target.kill()
                    arrow.kill()

        for slime in slimes:
            slimeCollisionRect = slime.getCollideRect()
            if arrows != []:
                if slimeCollisionRect.colliderect(arrowCollisionRect):
                    slime.kill()
                    arrow.kill()
            
        for arrow in arrows:
            if arrow.isDead():
                arrows.remove(arrow)

        for target in targets:
            if target.isDead():
                targets.remove(target)

        for slime in slimes:
            if slime.isDead():
                slimes.remove(slime)

        offset = Vector2(max(0,
                             min(archer.getX() + (archer.getWidth() // 2) -
                                 (SCREEN_SIZE[0] // 2),
                                 WORLD_SIZE[0] - SCREEN_SIZE[0])),
                         max(0,
                             min(archer.getY() + (archer.getHeight() // 2) -
                                 (SCREEN_SIZE[1] // 2),
                                 WORLD_SIZE[1] - SCREEN_SIZE[1])))

    pygame.quit()


if __name__ == '__main__':
    main()
