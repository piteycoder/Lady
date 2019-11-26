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
            x_pos = random.choice((random.randint(0, self.width/2 - self.bug_width*2),
                                   random.randint(self.width/2 + self.bug_width, self.width - self.bug_width)))
            y_pos = random.choice((random.randint(0, self.height/2 - self.bug_height*2),
                                   random.randint(self.height/2 + self.bug_height, self.height - self.bug_height)))
            self.ladybugs.append(Ladybug(x_pos, y_pos, random.randint(1, 5)/1000, random.randint(1, 5)/1000,
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
        self.player.move(1 / 20, 1 / 20)
        for ladybug in self.ladybugs:
            # if self.player.collides_with(ladybug):
                # return False
            x_dir = random.choice((-1, 1))
            y_dir = random.choice((-1, 1))
            ladybug.move(x_dir * random.randint(1, 5) / 100, y_dir * random.randint(1, 5) / 100)
        return True
