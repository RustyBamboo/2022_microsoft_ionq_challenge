#!/usr/bin/python3

from .level0 import Level0


class LevelController(object):
    '''
        High level controller for levels. This gives an interface to 
        the main game loop to access which level is being played and
        what entities to draw
    '''
    def __init__(self, constant_actors):
        self.current_level = 0

        self.levels = []

        self.levels.append(Level0(constant_actors))

    @property
    def level(self):
        if self.levels[self.current_level].done:
            self.current_level = self.current_level + 1
        if self.current_level > len(self.levels) - 1:
            return None
        return self.levels[self.current_level]

    @property
    def bullet(self):
        # retrieve bullet class
        return self.levels[self.current_level].constant_actors[-1]
