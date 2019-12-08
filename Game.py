import random
import pygame
import config
import os

from Objects.Ladybug import Ladybug
from Objects.Player import Player
from Objects.Caption import Caption


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
        self.score = 0
        self.caption = Caption("text", 20)

    def set_difficulty(self, num_of_ladybugs):
        self.num_of_ladybugs = num_of_ladybugs
        for i in range(self.num_of_ladybugs):
            x_pos = random.choice((random.randint(0, self.width / 2 - self.bug_width * 2),
                                   random.randint(self.width / 2 + self.bug_width, self.width - self.bug_width)))
            y_pos = random.choice((random.randint(0, self.height / 2 - self.bug_height * 2),
                                   random.randint(self.height / 2 + self.bug_height, self.height - self.bug_height)))
            self.ladybugs.append(Ladybug(x_pos, y_pos, random.randint(1, 5) / 1000, random.randint(1, 5) / 1000,
                                         self.bug_width,
                                         self.bug_height))

    def run(self):
        run = self.__menu()
        no_collision = True
        while run and no_collision:
            self.__screen_update()
            pygame.display.update()
            self.clock.tick(self.FPS)

            self.player.move(-self.player.x_speed / 10, -self.player.y_speed / 10)
            no_collision = self.__update_enemies_movements()
            self.score += 1 * self.num_of_ladybugs

            for event in pygame.event.get():
                run = self.__handle_events(event)
            self.__handle_keys(pygame.key.get_pressed())
        if not no_collision:
            pygame.time.wait(3000)
        pygame.quit()

    def __screen_update(self):
        self.__screen.fill((0, 0, 0))
        self.__screen.blit(self.player.img, (self.player.x, self.player.y))
        for ladybug in self.ladybugs:
            self.__screen.blit(ladybug.img, (ladybug.x, ladybug.y))
        self.__screen.blit(self.caption.text, (10, 10))

    def __update_enemies_movements(self):
        for ladybug in self.ladybugs:
            if self.player.collides_with(ladybug):
                return False
            x_dir = random.choice((-1, 1))
            y_dir = random.choice((-1, 1))
            ladybug.move(x_dir * random.randint(1, 5) / 25, y_dir * random.randint(1, 5) / 25)
        return True

    def __handle_events(self, event):
        if event.type == pygame.QUIT:
            return False
        return True

    def __handle_keys(self, keys):
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.player.move(0, -config.player_movespeed)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.player.move(0, config.player_movespeed)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.player.move(-config.player_movespeed, 0)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.player.move(config.player_movespeed, 0)

    def __menu(self):
        logo = pygame.image.load(os.path.join('Objects/imgs/ladybug-logo.png'))
        logo = pygame.transform.scale(logo, (300, 300))
        captions = {
            "Start": Caption("START", 50, config.colors.get("Grey")),
            "Quit": Caption("QUIT", 50, config.colors.get("Grey"))
        }
        pygame.time.wait(300)
        run = False
        while not run:
            self.__screen.fill((0, 0, 0))
            self.__screen.blit(logo, ((self.width-300)/2, (self.height-300)/2))
            x = int(config.window_width/4)
            x_pos = x
            for caption in captions.values():
                self.__screen.blit(caption.text, (x_pos, caption.size))
                x_pos += x
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.time.wait(500)
                    return False
        return run
