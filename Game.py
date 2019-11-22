import random

import pygame

from Objects.Ladybug import Ladybug


class Game(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.ladybugs = []
        self.bug_width = 30
        self.bug_height = 30

    def set_difficulty(self, num_of_ladybugs):
        for i in range(num_of_ladybugs):
            self.ladybugs.append(Ladybug(random.randint(0, self.width - self.bug_width),
                                         random.randint(0, self.height - self.bug_height),
                                         random.randint(1, 5),
                                         random.randint(1, 5),
                                         self.bug_width,
                                         self.bug_height))

    @staticmethod
    def run():
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
        pygame.quit()
