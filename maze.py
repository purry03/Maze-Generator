import pygame
from pygame import gfxdraw
import numpy as np
from noise import pnoise2
import random

pygame.init()
windowSize = 500
clock = pygame.time.Clock()
threshhold = 0.1
# Open a new window
size = (windowSize,windowSize)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Maze generator")

runGame = True

pixels = np.ones([windowSize,windowSize])

offset_x = random.random() * 10000
offset_y = random.random() * 10000

for i,row in enumerate(pixels):
    for j,column in enumerate(pixels):
        i1 = i/10 +offset_x
        j1 = j/10 +offset_y
        noise = np.absolute(pnoise2(i1, j1))
        pixels[i][j] = noise

for a in pixels:
    print(a)
while runGame:

    #handle quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runGame = False

    for i,row in enumerate(pixels):
        for j,column in enumerate(pixels):
            if not pixels[i][j] > threshhold:
                gfxdraw.pixel(screen, i, j, (255,255,255))

    pygame.display.flip()
    clock.tick(60)
