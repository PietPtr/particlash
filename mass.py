import pygame
import math
import numpy as np

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
            print("handling collision: ", self.newv)
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

        # apply force vector to position
        acc = f_res / self.mass
        self.vel += acc * dt
        self.pos += self.vel * dt
        #print(self.vel)

    def update_collisions(self, dt, masses):
        for mass in masses:
            if mass is self:
                continue

            r12 = np.linalg.norm(self.pos - mass.pos)   # distance

            if r12 < self.size + mass.size:
                v1 = self.vel
                v2 = mass.vel
                m1 = self.mass
                m2 = mass.mass

                #self.newv = (v1 * (m1 - m2) + (2 * m2 * v2)) / (m1 + m2)
                self.newv[0] = (v1[0] * (m1 - m2) + (2 * m2 * v2[0])) / (m1 + m2)
                self.newv[1] = (v1[1] * (m1 - m2) + (2 * m2 * v2[1])) / (m1 + m2)

                self.collided = True

                print (v1, v2, m1, m2, self.newv)

    def draw(self, screen):
        color = (247, 238, 195)

        if self.collided:
            color = (255, 0, 0)

        pygame.draw.circle(screen, color, (int(self.pos[0]), \
            int(self.pos[1])), self.size)
