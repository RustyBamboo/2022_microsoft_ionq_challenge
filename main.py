#!python3

from levels import *
from entities import *
import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
import time

import numpy as np

from qiskit import Aer, IBMQ
from qiskit.providers.aer import noise

from azure.quantum.qiskit import AzureQuantumProvider


SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
BOTTOM_BAR_HEIGHT = 50


def draw_loading_screen(screen, additional_text=None):
    '''
        Helper to draw loading screen "Loading + details"
    '''
    surf = pygame.Surface(screen.get_size())
    surfrect = surf.get_rect()
    surf.fill((130, 130, 130))
    font = pygame.font.Font(None, 36)
    text = font.render("Loading...", True, (255, 255, 255))
    textrect = text.get_rect(centerx=screen.get_width()/2,
                             centery=screen.get_height()/2 - 50)
    surf.blit(text, textrect)

    if additional_text is not None:
        font = pygame.font.Font(None, 26)
        text = font.render(additional_text, True, (255, 255, 255))
        textrect = text.get_rect(
            centerx=screen.get_width()/2, centery=screen.get_height()/2)
        surf.blit(text, textrect)

    screen.blit(surf, surfrect)

    pygame.display.update()


def draw_final_screen(screen):
    '''
        Helper to draw closing sreen
    '''
    surf = pygame.Surface(screen.get_size())
    surfrect = surf.get_rect()
    surf.fill((130, 130, 130))
    font = pygame.font.Font(None, 36)
    text = font.render("Ayyy go Quantum", True, (255, 255, 255))
    textrect = text.get_rect(centerx=screen.get_width()/2,
                             centery=screen.get_height()/2 - 50)
    surf.blit(text, textrect)
    pygame.display.update()


def main():
    pygame.init()
    pygame.display.set_caption("Leap through the Channel")
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    draw_loading_screen(screen)

    # Load IBMQ account and avaliable devices
    draw_loading_screen(screen, 'Loeading...')
    IBMQ.load_account()

    draw_loading_screen(screen, 'Getting least busy IBMQ device')
    provider = IBMQ.get_provider(group='open')
    provider = AzureQuantumProvider (
        resource_id = "/subscriptions/b1d7f7f8-743f-458e-b3a0-3e09734d716d/resourceGroups/aq-hackathons/providers/Microsoft.Quantum/Workspaces/aq-hackathon-01",
        location = "eastus"
    )

    real_backend = provider.get_backend("ionq.simulator")
    qpu_backend = provider.get_backend("ionq.qpu")

    draw_loading_screen(screen, 'Got {}'.format(real_backend.name()))
    if 0:
        # Use a real quantum device!
        draw_loading_screen(screen, 'Using {}'.format(real_backend.name()))
        execute_params = {'backend': real_backend}
    else:
        # Set up noise models for simulator
        properties = real_backend.properties()
        coupling_map = real_backend.configuration().coupling_map
        noise_model = noise.device.basic_device_noise_model(properties)
        basis_gates = noise_model.basis_gates

        sim_backend = Aer.get_backend('qasm_simulator')
        draw_loading_screen(screen, 'Using {} with {} noise model'.format(
            sim_backend.name(), real_backend.name()))
        execute_params = {'backend': sim_backend, 'coupling_map': coupling_map,
                          'noise_model': noise_model, 'basis_gates': basis_gates}

    # Give time to read updated loading screen
    time.sleep(2)

    # Construct our main compenents
    dim = (SCREEN_WIDTH, SCREEN_HEIGHT, BOTTOM_BAR_HEIGHT)
    player = Player()
    bullet = BulletManager(dim, execute_params)
    bulletEC = BulletManagerEC(dim, execute_params)
    dashboard = Dashboard(bullet, dim)

    # Default level
    level_controller = LevelController((dashboard, player, bullet))

    # Add level with error-correcting bullets
    level_controller.levels.append(Level0((dashboard, player, bulletEC)))

    while 1:

        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    # Fire bullet
                    level_controller.bullet.call_fire()
                    player.increase_shots()

                # Switch the weapon
                if event.key == K_RIGHT:
                    dashboard.update_gates(1)
                    bullet.prepare()
                if event.key == K_LEFT:
                    dashboard.update_gates(-1)
                    bullet.prepare()

                # Switch out lens - i.e. measurement basis
                if event.key == K_UP:
                    dashboard.update_measure_basis(1)
                if event.key == K_DOWN:
                    dashboard.update_measure_basis(-1)

        # Get current level and update it
        l = level_controller.level
        if l is None:
            print("Fini")
            return
        l.update()
        l.draw(screen)

        pygame.display.flip()


if __name__ == '__main__':
    main()
    pygame.quit()
