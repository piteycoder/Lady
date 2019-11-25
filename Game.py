import random
import pygame


from Objects.Ladybug import Ladybug
from Objects.Player import Player


class Game(object):

    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.__screen = pygame.display.set_mode((self.width, self.height))
        self.ladybugs = []
        self.bug_width = 30
        self.bug_height = 30
        self.p_width = 30
        self.p_height = 30
        self.player = Player((self.width - self.p_width) / 2, (self.height - self.p_height) / 2, 0, 0,
                             self.p_width, self.p_height)
        self.num_of_ladybugs = 0
        self.FPS = 60
        self.clock = pygame.time.Clock()

    def set_difficulty(self, num_of_ladybugs):
        self.num_of_ladybugs = num_of_ladybugs
        for i in range(self.num_of_ladybugs):
            self.ladybugs.append(Ladybug(random.randint(0, self.width - self.bug_width),
                                         random.randint(0, self.height - self.bug_height),
                                         random.randint(1, 5),
                                         random.randint(1, 5),
                                         self.bug_width,
                                         self.bug_height))

    def run(self):
        run = True
        while run:
            run = self.__update_movements()
            self.__screen_update()
            pygame.display.update()
            self.clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
        pygame.quit()

    def __screen_update(self):
        self.__screen.fill((0, 0, 0))
        self.__screen.blit(self.player.img, (self.player.x, self.player.y))
        for ladybug in self.ladybugs:
            self.__screen.blit(ladybug.img, (ladybug.x, ladybug.y))

    def __update_movements(self):
        self.player.move(1/20, 1/20)
        for ladybug in self.ladybugs:
            if self.player.collides(ladybug):
                return False
            ladybug.move(random.randint(1, 5)/1000, random.randint(1, 5)/1000)
        return True
