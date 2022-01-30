#!/usr/bin/python3

from .level import Level
from entities import Enemy

import pygame


class Level0(Level):
    def __init__(self, constant_actors):
        super(Level0, self).__init__(constant_actors)
        screen = pygame.display.get_surface()
        pos = screen.get_width()/2 - 100, 12
        self.enemies.append(Enemy(pos))

    def trigger_enemy_killed(self):
        '''
            3 stages to clear, each stage being constructed when a number 
            of enemies have been killed.
        '''
        screen = pygame.display.get_surface()
        if self.enemies_killed < 4:
            if self.enemies_killed == 1:
                pos = screen.get_width()/2 + 100, 12
                self.enemies.append(Enemy(pos))
            if self.enemies_killed == 2:
                pos = screen.get_width()/2 + 100, screen.get_height()/2 - 50
                self.enemies.append(Enemy(pos))

                pos = screen.get_width()/2 - 100, screen.get_height()/2 - 50
                self.enemies.append(Enemy(pos))
        else:
            self.done = True
