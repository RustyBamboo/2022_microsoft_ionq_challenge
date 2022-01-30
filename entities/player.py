#!/usr/bin/python

import pygame


class Player(pygame.sprite.Sprite):
    '''
        Simple player singleton which displays how many bullets have been shot
    '''

    def __init__(self):
        self.shots = 0
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()

        screen = pygame.display.get_surface()
        self.rect.topleft = screen.get_width()/2 - self.rect.width / \
            2, screen.get_height() - self.rect.height/2 - 25
        self.image = self.surf
        self.font = pygame.font.Font(None, 26)

    def reset_shots(self):
        self.shots = 0

    def increase_shots(self):
        self.shots = self.shots + 1

    def update(self):
        pass

    def draw(self, screen):
        t = str(self.shots)
        text = self.font.render(t, True, (0, 0, 0))
        textrect = text.get_rect()
        textrect.center = self.surf.get_width()/2, self.surf.get_height()/2
        self.image = self.surf.copy()
        self.image.blit(text, textrect)

        screen.blit(self.image, self.rect)
