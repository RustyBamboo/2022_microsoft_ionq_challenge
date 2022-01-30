#!/usr/bin/python

import pygame


class Dashboard(pygame.sprite.Sprite):
    def __init__(self, bullet, dim):
        self.screen_width, self.screen_height, self.bottom_bar_height = dim
        super(Dashboard, self).__init__()

        # Possible set of gates
        self.possible_gates = ['X', 'Y', 'Z', 'H']
        self.possible_measure_basis = ['X', 'Y', 'Z', 'H']

        # Which gate is currently selected
        self.gate_cycle = 3
        self.measure_basis_cycle = 3

        # What to draw on dashboard
        self.gates = self.possible_gates[self.gate_cycle]
        self.measure_basis = self.possible_measure_basis[self.measure_basis_cycle]

        # Get reference to the bullet manager to control when we have update
        self.bullet = bullet
        self.bullet.update_gates(self.gates)

        self._generate_surf()
        self.font = pygame.font.Font(None, 26)
        self.rect = self.surf.get_rect(
            topleft=(0, self.screen_height - self.bottom_bar_height))

        self.update_gates(1)
        self.update_measure_basis(1)

    def _generate_surf(self):
        self.surf = pygame.Surface((self.screen_width, self.bottom_bar_height))
        self.surf.fill((0, 100, 100))

    def update_gates(self, of):
        self.gate_cycle = (self.gate_cycle + of) % len(self.possible_gates)
        self.gates = self.possible_gates[self.gate_cycle]
        self.bullet.update_gates(self.gates)

    def update_measure_basis(self, of):
        self.measure_basis_cycle = (
            self.measure_basis_cycle + of) % len(self.possible_measure_basis)
        self.measure_basis = self.possible_measure_basis[self.measure_basis_cycle]
        self.bullet.update_measure_basis(self.measure_basis)

    def draw(self, screen):

        # Draw current gate
        t = str(self.gates)
        if t == 'H':
            t = 'Hadafire'
        if t == 'X':
            t = 'X-Bringer'
        if t == 'Y':
            t = 'Y-Bringer'
        if t == 'Z':
            t = 'Z-Bringer'

        text = self.font.render(t, True, (255, 255, 255))
        textrect = text.get_rect()
        self.image = self.surf.copy()
        self.image.blit(text, textrect)

        # Draw the basis text
        t = str(self.measure_basis)
        text = self.font.render("Lens: " + t, True, (255, 255, 255))
        textrect = text.get_rect()
        textrect.right = self.screen_width
        self.image.blit(text, textrect)

        screen.blit(self.image, self.rect)
