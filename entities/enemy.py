#!usr/bin/python

import pygame

import numpy as np


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        self.pos = pos
        # The radius of the circle for enemy to move around
        self.radius = 10
        self.angle = 0
        # Randomize the direction of rotating
        self.direction = np.random.randint(0, 2) * 2 - 1

        super(Enemy, self).__init__()
        self.surf = pygame.Surface((25, 25))
        self.surf.fill((255, 0, 0))
        self.image = self.surf
        self.rect = self.surf.get_rect()
        self.rect.center = pos[0], pos[1]

    def update(self):
        # Each tick change the position of enemy along a circle
        x, y = self.pos
        self.angle = self.angle + self.direction * 0.005
        if self.angle > 2 * np.pi or self.angle < -2 * np.pi:
            self.angle = 0
        nx = x + self.radius * np.cos(self.angle)
        ny = y + self.radius * np.sin(self.angle)
        self.rect.center = nx, ny

    def draw(self, screen):
        screen.blit(self.image, self.rect)
