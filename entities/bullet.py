#!usr/bin/python

import pygame

from qiskit import qiskit, ClassicalRegister, QuantumRegister, QuantumCircuit, Aer

from qiskit.providers import JobStatus

import numpy as np


class BulletManager(object):
    '''
        Main class for constructing and running quantum algorithm.
        The results are then measured and the bullets are mapped.
    '''
    def __init__(self, dim, execute_params):
        '''
            dim: the width, height, and dashboard height
            execute_params: additional params for qiskit execute
        '''
        self.screen_width, self.screen_height, self.bottom_bar_height = dim

        # Crate bullets that are offset
        self.lbullet = Bullet(self.screen_width/2 - 100)
        self.rbullet = Bullet(self.screen_width/2 + 100)

        # pygame quick rendering
        self.allsprites = pygame.sprite.RenderPlain(
            (self.lbullet, self.rbullet))

        self.execute_params = execute_params

        # Bool to check if quantum prgram is running
        self.calculating = False
        self.gates = 'X'
        self.measure_basis = 'X'
        self._reset_position()
        self.prepare()

        # Instead of setting to None, set to small number for first compare with current time
        self.fire_time = -10000

    def prepare(self):
        '''
            Construct quantum circuit
        '''
        self.circ = QuantumCircuit(2, 1)

        for g in self.gates:
            if g == 'H':
                self.circ.h(0)
            if g == 'X':
                self.circ.x(0)
            if g == 'Y':
                self.circ.y(0)
            if g == 'Z':
                self.circ.z(0)
        self.circ.cx(0, 1)

    def call_fire(self):
        '''
            Entry function to call the main fire method
        '''
        self.fire()

    def fire(self):
        self.calculating = True

        circ = self.circ.copy()

        if self.measure_basis is not None:
            if self.measure_basis == 'H':
                circ.h(1)
            if self.measure_basis == 'X':
                circ.x(1)
            if self.measure_basis == 'Y':
                circ.y(1)
            if self.measure_basis == 'Z':
                circ.z(1)

        circ.measure(1, 0)
        self.shots = 1024 * 4
        self.job = qiskit.execute(
            circ, **self.execute_params, shots=self.shots)

    def _handle_post_fire(self):
        '''
            Handles mapping the prob of 0 or 1 to y coordinate
        '''
        his = self.job.result().get_counts()

        if '0' not in his:
            his['0'] = 0
        if '1' not in his:
            his['1'] = 0

        screen = pygame.display.get_surface()
        self.lbullet.rect.top = his['0'] / self.shots * \
            (screen.get_height() - self.bottom_bar_height - self.lbullet.diffy)

        self.rbullet.rect.top = his['1'] / self.shots * \
            (screen.get_height() - self.bottom_bar_height - self.rbullet.diffy)

        self.fire_time = pygame.time.get_ticks()

    def _loading_animation(self):
        '''
            Animation to display that quantum circuit is being run
        '''
        self.lbullet.surf.fill(
            (255 * np.random.rand(), 0, 255 * np.random.rand()))
        self.rbullet.surf.fill(
            (255 * np.random.rand(), 0, 255 * np.random.rand()))

    def _reset_position(self):
        self.lbullet.rect.centerx = self.lbullet.posx
        self.lbullet.rect.centery = self.screen_height - self.bottom_bar_height - 8
        self.rbullet.rect.centerx = self.rbullet.posx
        self.rbullet.rect.centery = self.screen_height - self.bottom_bar_height - 8

    def update(self):
        '''
            Each tick check if we are calculating a quantum program
        '''
        if self.calculating:
            self._loading_animation()
            # If done, then we can reset everything
            if self.job.status() == JobStatus.DONE:
                self._handle_post_fire()
                self.calculating = False
                self.lbullet.set_color(self.measure_basis)
                self.rbullet.set_color(self.measure_basis)

    def update_gates(self, gates):
        # Change our weapon
        self.gates = gates

    def update_measure_basis(self, measure_basis):
        self.measure_basis = measure_basis
        self.lbullet.set_color(self.measure_basis)
        self.rbullet.set_color(self.measure_basis)

    def draw(self, screen):
        if pygame.time.get_ticks() - self.fire_time < 100:
            if self.calculating is False:
                def draw_rainbow(s, e, reverse=False):
                    x1, y1 = s
                    x2, y2 = e
                    colors = [(148, 0, 211),
                              (75, 0, 130),
                              (0, 0, 255),
                              (0, 255, 0),
                              (255, 255, 0),
                              (255, 127, 0),
                              (255, 0, 0), ]

                    if reverse:
                        colors = colors[::-1]

                    for i in range(7):
                        of = i - 3
                        c = colors[i]
                        pygame.draw.line(
                            screen, c, (x1+of, y1), (x2+of, y2), 2)

                # Draw animation of bullet firing via a rainbow
                draw_rainbow((self.lbullet.posx, self.screen_width -
                              self.bottom_bar_height), self.lbullet.rect.center)
                draw_rainbow((self.rbullet.posx, self.screen_width -
                              self.bottom_bar_height), self.rbullet.rect.center, True)

        self.allsprites.draw(screen)


class BulletManagerEC(BulletManager):
    '''
        Error correcting version for bullet
    '''

    def __init__(self, dim, execute_params):
        super(BulletManagerEC, self).__init__(dim, execute_params)

    def prepare(self):
        # Index of ancilla qubit
        ancilla1 = 0
        # Index of qubit
        qub = 1
        self.circ = QuantumCircuit(5, 5)

        # Initial logical |00> state preperation
        self.circ.h(qub)
        self.circ.cx(qub, ancilla1)
        for q in range(1, 4):
            self.circ.cx(qub, qub + q)
        self.circ.cx(qub, ancilla1)
        self.circ.measure(ancilla1, ancilla1)
        self.circ.barrier()

        for g in self.gates:
            if g == 'X':
                self.circ.x(qub)
                self.circ.iden(qub+1)
                self.circ.x(qub+2)
                self.circ.iden(qub+3)
            if g == 'Z':
                self.circ.z(qub)
                self.circ.z(qub+1)
                self.circ.iden(qub+2)
                self.circ.iden(qub+3)
            if g == 'H':
                for q in range(0, 4):
                    self.circ.h(qub+q)

            #self.circ.swap(qub, qub + 1)

        #self.circ.measure(ancilla2, ancilla2)

    def fire(self):
        self.calculating = True

        circ = self.circ.copy()

        for q in range(0, 4):
            circ.measure(1 + q, 1 + q)

        self.shots = 1024 * 4
        self.job = qiskit.execute(
            circ, **self.execute_params, shots=self.shots)

    def _handle_post_fire(self):
        his = self.job.result().get_counts()
        s = sorted(his.items(), key=lambda item: item[1])

        his_s = []
        cnt = 0
        for k, v in s:
            # if ancilla is nonzero then there was an error, so ignore
            if k[-1] != '0':
                continue
            ks = k[0:4][::-1]
            # Take states that are only in the code
            if ks == '0000' or ks == '1111' or ks == '0011' or ks == '1100' or ks == '0101' or ks == '1010' or ks == '0110' or ks == '1001':
                his_s.append((ks, v))
                cnt = cnt + v**2
        
        # renormalize those states
        his_s = {k: v/np.sqrt(cnt) for k, v in his_s}

        # map to logical qubits
        state_00 = 1/np.sqrt(2) * (his_s['0000'] + his_s['1111'])
        state_01 = 1/np.sqrt(2) * (his_s['0011'] + his_s['1100'])
        state_10 = 1/np.sqrt(2) * (his_s['0101'] + his_s['1010'])
        state_11 = 1/np.sqrt(2) * (his_s['0110'] + his_s['1001'])

        #print(state_00, state_01, state_10, state_11)

        # multiply by 2 because need to remove 1/sqrt(2) to get probability
        s0 = state_00 * state_10 * 2
        s1 = state_01 * state_11 * 2

        svec = np.array([[s0], [s1]])
        # jank change of basis
        if self.measure_basis is not None:
            if self.measure_basis == 'H':
                svec = np.array([[1, 1], [1, -1]]).dot(svec) / np.sqrt(2)
            if self.measure_basis == 'X':
                svec = np.array([[0, 1], [1, 0]]).dot(svec)
            if self.measure_basis == 'Y':
                svec = np.array([[0, -1j], [1j, 0]]).dot(svec)
            if self.measure_basis == 'Z':
                svec = np.array([[1, 0], [0, -1]]).dot(svec)

        svec = np.abs(svec)
        s0 = svec[0][0]
        s1 = svec[1][0]

        screen = pygame.display.get_surface()

        self.lbullet.rect.top = s0 * \
            (screen.get_height() - self.bottom_bar_height - self.lbullet.diffy)

        self.rbullet.rect.top = s1 * \
            (screen.get_height() - self.bottom_bar_height - self.rbullet.diffy)
        self.fire_time = pygame.time.get_ticks()


class Bullet(pygame.sprite.Sprite):
    '''
        Bullet class that holds sprite and position information
    '''

    def __init__(self, posx):
        self.posx = posx
        super(Bullet, self).__init__()
        self.surf = pygame.Surface((15, 15))
        self.surf.fill((255, 255, 0))
        self.image = self.surf
        self.rect = self.surf.get_rect()

    @property
    def diffx(self):
        return self.surf.get_width()

    @property
    def diffy(self):
        return self.surf.get_height()

    def set_color(self, gate):
        d = ord(gate) // 1 % 10
        dd = ord(gate) // 10 % 10

        self.surf.fill((10, (d * 10 + dd + 15)*10 %
                        255, (d * 10 + dd)*10 % 255))
