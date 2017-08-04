import sys
import pygame
import numpy as np
from mass import Mass
import random as r

pygame.init()

size = width, height = 1000, 1000
black = 0, 0, 0
white = 255, 255, 255

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

masses = []

preset = "lagrange"

if preset == "gas":
    XPAD = 200
    YPAD = 200
    MINMAX = 200
    for x in range(0, int(width / XPAD)):
        for y in range(0, int(height / YPAD)):
            masses.append(Mass(np.array([XPAD / 2 + x * XPAD, YPAD / 2 + y * YPAD]),\
                np.array([r.uniform(-MINMAX, MINMAX), r.uniform(-MINMAX, MINMAX)]), 10))

elif preset == "three":
    masses.append(Mass(np.array([500.0, 300.0]), np.array([0.0, 0.0]), 20))
    masses.append(Mass(np.array([630.0, 300.0]), np.array([0.0, 0.0]), 20))
    masses.append(Mass(np.array([600.0, 400.0]), np.array([0.0, 0.0]), 20))
elif preset == "lagrange":
    masses.append(Mass(np.array([367.0, 456.0]), np.array([39.5, -148.3]), 1))
    masses.append(Mass(np.array([500.0, 350.0]), np.array([150.0, 0.0]), 10))
    masses.append(Mass(np.array([500.0, 500.0]), np.array([0.0, 0.0]), 50))
elif preset == "quad":
    SPEED = 122
    masses.append(Mass(np.array([500.0, 300.0]), np.array([-SPEED, 0.0]), 50))
    masses.append(Mass(np.array([300.0, 500.0]), np.array([0.0, SPEED]), 50))
    masses.append(Mass(np.array([500.0, 700.0]), np.array([SPEED, 0.0]), 50))
    masses.append(Mass(np.array([700.0, 500.0]), np.array([0.0, -SPEED]), 50))
elif preset == "world":
    masses.append(Mass(np.array([500.0, 300.0]), np.array([55.0, 0.0]), 5))
    masses.append(Mass(np.array([500.0, 500.0]), np.array([0.0, 0.0]), 100))
elif preset == "impulse":
    masses.append(Mass(np.array([500.0, 500.0]), np.array([0.0, 0.0]), 100))
    masses.append(Mass(np.array([100.0, 540.0]), np.array([1000.0, 0.0]), 10))

view = [0, 0]
zoom = 1

frame = 0
history_drawn = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                zoom *= 1.1
            if event.button == 5:
                zoom /= 1.1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                history_drawn -= 1
            if event.key == pygame.K_RIGHT:
                history_drawn += 1
            if event.key == pygame.K_v:
                total = 0
                for mass in masses:
                    total += np.linalg.norm(mass.vel)
                print("total speed: ", total)
            if event.key == pygame.K_p:
                masses[history_drawn].vel *= 1.5
    """
    Updates and logic
    """
    dt = clock.tick() / 1000.0

    if history_drawn < 0:
        history_drawn = len(masses) - 1
    if history_drawn > len(masses) - 1:
        history_drawn = 0

    if frame % 60 == 0 and dt != 0:
        pass#print (1 / dt)

    mov = pygame.mouse.get_rel()
    if (pygame.mouse.get_pressed()[0]):
        view[0] += mov[0] * 1 / zoom
        view[1] += mov[1] * 1 / zoom

    for mass in masses:
        mass.update(dt, masses)

    for mass in masses:
        mass.apply_move(dt)

    frame += 1
    """
    Drawing
    """
    screen.fill(black)

    count = 0
    for mass in masses:
        mass.draw(screen, view, zoom, frame, count == history_drawn)
        count += 1

    pygame.display.flip()
