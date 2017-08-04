import sys
import pygame
import numpy as np
from mass import Mass

pygame.init()

size = width, height = 1280, 720
black = 0, 0, 0
white = 255, 255, 255

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

masses = []

XPAD = 128
YPAD = 128
# for x in range(0, int(width / XPAD)):
#     for y in range(0, int(height / YPAD)):
#         masses.append(Mass(np.array([XPAD / 2 + x * XPAD, YPAD / 2 + y * YPAD]),\
#             np.array([0.0, 0.0]), 10))
#
masses.append(Mass(np.array([100.0, 145.0]), np.array([50.0, 0.0]), 30))
masses.append(Mass(np.array([200.0, 100.0]), np.array([-10.0, 0.0]), 30))

# masses.append(Mass(np.array([150.0, 100.0]), np.array([100, 0.0]), 10))
# masses.append(Mass(np.array([200.0, 200.0]), np.array([0.0, -200.0]), 10))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    dt = clock.tick() / 1000.0

    """
    Updates and logic
    """
    for mass in masses:
        mass.update(dt, masses)

    for mass in masses:
        mass.apply_move(dt)

    """
    Drawing
    """
    screen.fill(black)

    for mass in masses:
        mass.draw(screen)

    pygame.display.flip()
