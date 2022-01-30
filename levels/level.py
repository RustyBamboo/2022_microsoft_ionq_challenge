#!/usr/bin/python3
import pygame

from entities import BulletManager


class Level(object):
    '''
        High level parent class to create levels
    '''
    def __init__(self, constant_actors):
        self.constant_actors = constant_actors
        self.enemies = []
        self.enemies_killed = 0
        self.done = False

    def update(self):
        # Update all of the entities
        for a in self.constant_actors:
            a.update()
            # Check for collision of bullets
            if isinstance(a, BulletManager):
                for e in self.enemies:
                    self.check_collision(a, e)

        for e in self.enemies:
            e.update()

    def draw(self, screen):
        for a in self.constant_actors:
            a.draw(screen)

        for e in self.enemies:
            e.draw(screen)

    def check_collision(self, a, e):
        # If either of the bullets hit then we need to process
        if a.lbullet.rect.colliderect(e.rect) or a.rbullet.rect.colliderect(e.rect):
            self.handle_collision(e)

    def handle_collision(self, e):
        self.enemies_killed = self.enemies_killed + 1
        self.enemies.remove(e)
        self.trigger_enemy_killed()

    def trigger_enemy_killed(self):
        # what to do when an enemy was hit
        pass
