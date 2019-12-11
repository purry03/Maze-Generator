import pygame
from pygame import gfxdraw
import numpy as np
from noise import pnoise2
import random
from timeit import default_timer as timer


if __name__ == "__main__":
    pygame.init()
    windowSize = 500
    clock = pygame.time.Clock()
    threshhold = 0.1
    # Open a new window
    size = (windowSize, windowSize)
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Maze generator")

    runGame = True

    start = timer()
    pixels = np.zeros(size)

    offset_x = random.randint(0, 10000)
    offset_y = random.randint(0, 10000)

    for i in range(windowSize):
        i1 = i / 10 + offset_x
        for j in range(windowSize):
            j1 = j / 10 + offset_y
            noise = abs(pnoise2(i1, j1))
            pixels[i][j] = noise

    end = timer()
    print("%f seconds elapsed." % (end - start))

    while runGame:

        # handle quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runGame = False

        for i in range(windowSize):
            for j in range(windowSize):
                if not pixels[i][j] > threshhold:
                    gfxdraw.pixel(screen, i, j, (255, 255, 255))

        pygame.display.flip()
        clock.tick(60)
