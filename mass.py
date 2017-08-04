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

            #f_res += f_grav

        acc = f_res / self.mass
        self.vel += acc * dt

        # collision stuff
        for B in masses:
            if B is self:
                continue

            A = self

            v = self.vel - mass.vel

            dist = np.linalg.norm(A.pos - B.pos)
            sumRadii = A.size + B.size
            dist -= sumRadii

            if (np.linalg.norm(v) < dist):
                log("Cant hit...")
                continue

            N = v / np.linalg.norm(v)

            C = B.pos - A.pos

            D = np.dot(N, C)

            if (D <= 0):
                log("Not towards B...")
                continue

            lenC = np.linalg.norm(C)

            F = (lenC ** 2) - (D ** 2)

            if (F >= sumRadii ** 2):
                log("Not close enough...")
                continue

            T = sumRadii ** 2 - F

            if T < 0:
                log("No triangle available...")
                continue

            distance = D - math.sqrt(T)

            mag = np.linalg.norm(v) * dt

            if (mag < distance):
                log("Dist req higher than vel...")
                continue

            self.vel = distance * N

            log("Collision?")


    def apply_move(self, dt):
        # apply force vector to position
        self.pos += self.vel * dt
        #log(self.vel)


    def draw(self, screen):
        color = (247, 238, 195)

        if self.collided:
            color = (255, 0, 0)

        pygame.draw.circle(screen, color, (int(self.pos[0]), \
            int(self.pos[1])), self.size)

        pygame.draw.circle(screen, (0, 0, 0), (int(self.pos[0]), \
            int(self.pos[1])), 0)
