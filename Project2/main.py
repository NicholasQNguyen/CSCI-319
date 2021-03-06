"""
Author: Nicholas Nguyen
Project 1
File: main.py
"""
import pygame
import os
from vector2D import Vector2
from orb import Orb
from star import Star
from highScore import HighScore
from copy import deepcopy

# Two different sizes now! Screen size is the amount we show the player,
#  and world size is the size of the interactable world
SCREEN_SIZE = Vector2(800, 800)
WORLD_SIZE = Vector2(1200, 1200)


def main():
    # initialize the pygame module
    pygame.init()

    # load and set the logo
    pygame.display.set_caption("Nicholas Nguyen Project 2")

    screen = pygame.display.set_mode(list(SCREEN_SIZE))

    # Let's make a background so we can see if we're moving
    background = pygame.image.load(os.path.join("background.png")).convert()

    # Star images
    star = Star()
    star._image.convert()
    star._image.set_colorkey(star._image.get_at((0, 0)))

    # List of orbs
    orbs = []
    # The offset of the window into the world
    offset = Vector2(0, 0)

    # Message stuff to handle score tracking
    scoreMessage = HighScore()
    screenWidth = Vector2(0, 0)

    gameClock = pygame.time.Clock()

    # define a variable to control the main loop
    RUNNING = True

    # main loop
    while RUNNING:

        # Draw everything, adjust by offset
        screen.blit(background, (-offset.x, -offset.y))
        star.draw(screen, offset)

        # Put the score in the top right following the camera
        screenWidth[0] = screen.get_width() - scoreMessage.getImage().get_width()
        screen.blit(scoreMessage.getImage(), list(screenWidth))

        for orb in orbs:
            orb.draw(screen, offset)

        # Flip the display to the monitor
        pygame.display.flip()

        # event handling, gets all event from the eventqueue
        for event in pygame.event.get():
            # only do something if the event is of type
            # QUIT or ESCAPE is pressed
            if event.type == pygame.QUIT or \
               (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                # change the value to False, to exit the main loop
                RUNNING = False

            elif event.type == pygame.KEYDOWN:
                star.handleEvent(event)

            elif event.type == pygame.KEYUP:
                star.handleEvent(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                adjustedPos = list(event.pos)
                adjustedPos[0] += offset[0]
                adjustedPos[1] += offset[1]
                # Generate an orb
                orb = Orb(adjustedPos)
                orb._image.convert()
                orb._image.set_colorkey(orb._image.get_at((0, 0)))

                # Append the generated orb to the list
                orbs.append(orb)

        gameClock.tick(60)

        ticks = gameClock.get_time() / 1000

        # Update everything
        star.update(WORLD_SIZE, ticks)
        for orb in orbs:
            orb.update(WORLD_SIZE, ticks)

        # Set up a collision rectangle for the star and
        # move it to where the star currently is
        starCollisionRect = star.getCollideRect()
        starCollisionRect.move_ip(star.getX(), star.getY())

        # Iterate through the orbs, generate a collision rectangle
        # for each orb and move the collision rectangle to where each orb it
        for orb in orbs:
            orbCollisionRect = orb.getCollideRect()
            orbCollisionRect.move_ip(orb.getX(), orb.getY())

            # If the star and an orb's collisions hit, kill the orb
            if orbCollisionRect.colliderect(starCollisionRect):
                orb.kill()
                # Increase the score by 1 for each orb hit
                scoreMessage.iterateScore()
                # Fill the surface the score is on to hide the old score
                scoreMessage.getImage().fill((0, 0, 0))
                # Update the score with the new score
                scoreMessage.updateMessage()

        # Clear out orbs that are dead
        for orb in orbs:
            if orb.isDead():
                orbs.remove(orb)

        # Recalculate the offest based on the new position
        offset = Vector2(max(0,
                             min(star.getX() + (star.getWidth() // 2) -
                                 (SCREEN_SIZE[0] // 2),
                                 WORLD_SIZE[0] - SCREEN_SIZE[0])),
                         max(0,
                             min(star.getY() + (star.getHeight() // 2) -
                                 (SCREEN_SIZE[1] // 2),
                                 WORLD_SIZE[1] - SCREEN_SIZE[1])))

    pygame.quit()


if __name__ == "__main__":
    main()
