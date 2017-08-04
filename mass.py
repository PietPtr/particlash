import pygame
import math
import numpy as np
from util import log

DENSITY = 1
HISTORY = True
GRAVITY = False

class Mass(object):
    def __init__(self, pos, vel, size):
        self.pos = pos
        self.vel = vel
        self.size = size
        self.mass = 4/3 * math.pi * math.pow(size, 3) * DENSITY
        self.newv = np.array([0.0, 0.01])
        self.collided = False
        self.history = []

    def update(self, dt, masses):
        # calculate new force vector
        f_res = np.array([0.0, 0.0])

        if self.collided:
            log("handling collision: ", self.newv)
            self.pos += self.newv * dt
            self.vel = self.newv
            self.newv = np.array([0.0, 0.0])
            self.collided = False

        if GRAVITY:
            for mass in masses:
                if mass is self:
                    continue

                m1  = self.mass
                m2  = mass.mass
                G   = 6.67408 * math.pow(10, 0)            # G for the lazy god
                r12 = np.linalg.norm(self.pos - mass.pos)   # distance
                ru  = (self.pos - mass.pos) / r12           # unit vector

                f_grav = (-G * (m1 * m2) / math.pow(r12, 2)) * ru

                f_res += f_grav

        acc = f_res / self.mass
        self.vel += acc * dt

        # collision stuff
        for mass in masses:
            if mass is self:
                continue

            if np.linalg.norm(self.pos - mass.pos) > mass.size + self.size:
                # no collision, carry on
                continue



            v1 = self.vel
            v2 = mass.vel

            x1 = self.pos
            x2 = mass.pos

            m1 = self.mass
            m2 = mass.mass

            vel = v1 - (2 * m2 / (m1 + m2)) * (np.dot(v1 - v2, x1 - x2)\
                / (np.linalg.norm(x2 - x1) ** 2)) * (x1 - x2)

            #vel = vel * 0.9

            self.vel_after_collision = vel
            self.collided = True

        if self.pos[0] - self.size < 0 or self.pos[0] + self.size > 1000:
            self.vel_after_collision = self.vel * [-1, 1]
            self.collided = True
        if self.pos[1] - self.size < 0 or self.pos[1] + self.size > 1000:
            self.vel_after_collision = self.vel * [1, -1]
            self.collided = True


    def apply_move(self, dt):
        # apply force vector to position
        if self.collided:
            self.collided = False
            self.vel = self.vel_after_collision

        self.pos += self.vel * dt
        #log(self.vel)


    def draw(self, screen, view, zoom, frame, draw_history):
        color = (247, 238, 195)

        if HISTORY:
            if frame % 10 == 0:
                self.history.append(self.pos.tolist())
                if len(self.history) > 50:
                    del self.history[0]

            if len(self.history) >= 2 and draw_history:
                pygame.draw.lines(screen, (100, 100, 100), False, self.history)
                color = (255, 100, 100)


        x = int((self.pos[0] + view[0]) * zoom)
        y = int((self.pos[1] + view[1]) * zoom)

        pygame.draw.circle(screen, color, (x, y), int(self.size * zoom))

        pygame.draw.circle(screen, (0, 0, 0), (x, y), 0)
