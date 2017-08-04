import pygame
import math
import numpy as np
from util import log

DENSITY = 1

class Mass(object):
    def __init__(self, pos, vel, size):
        self.pos = pos
        self.vel = vel
        self.size = size
        self.mass = 4/3 * math.pi * math.pow(size, 3) * DENSITY
        self.newv = np.array([0.0, 0.01])
        self.collided = False

    def update(self, dt, masses):
        # calculate new force vector
        f_res = np.array([0.0, 0.0])

        if self.collided:
            log("handling collision: ", self.newv)
            self.pos += self.newv * dt
            self.vel = self.newv
            self.newv = np.array([0.0, 0.0])
            self.collided = False

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

            print("collision between: ", self, mass, ", old: ", self.vel, ", new:", vel)

            self.vel_after_collision = vel
            self.collided = True



    def apply_move(self, dt):
        # apply force vector to position
        if self.collided:
            self.collided = False
            self.vel = self.vel_after_collision

        self.pos += self.vel * dt
        #log(self.vel)


    def draw(self, screen, view):
        color = (247, 238, 195)

        if self.collided:
            color = (255, 0, 0)

        x = int(self.pos[0]) + view[0]
        y = int(self.pos[1]) + view[1]

        pygame.draw.circle(screen, color, (x, y), self.size)

        pygame.draw.circle(screen, (0, 0, 0), (x, y), 0)
