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
        self.player = Player((self.width - 30) / 2, (self.height - 30) / 2, 0, 0)
        self.num_of_ladybugs = 0
        self.FPS = 60
        self.clock = pygame.time.Clock()
        self.score = 0
        self.caption = Caption("text", 20)

    def __set_difficulty(self, num_of_ladybugs=20):
        self.num_of_ladybugs = num_of_ladybugs
        for i in range(self.num_of_ladybugs):
            x_pos = random.choice((random.randint(0, self.width / 2 - 60),
                                   random.randint(self.width / 2 + 30, self.width - 30)))
            y_pos = random.choice((random.randint(0, self.height / 2 - 60),
                                   random.randint(self.height / 2 + 30, self.height - 30)))
            self.ladybugs.append(Ladybug(x_pos, y_pos, random.randint(1, 5) / 1000, random.randint(1, 5) / 1000))

    def run(self):
        menu = self.Menu(self.width, self.height)
        menu.run()
        start = Caption("WCIŚNIJ SPACJĘ ABY ROZPOCZĄĆ", 30, config.colors.get("White"))
        start.x = (self.width - start.text.get_width()) / 2
        start.y = int(self.height * 0.7)
        self.__screen_update([start])
        game = self.__get_space()
        while game:
            run = True
            collision = False
            self.score = 0
            start.y = int(self.height*0.7)
            self.__set_difficulty()
            self.__reset_player()
            while run and not collision:
                self.__screen_update()
                self.clock.tick(self.FPS)

                self.player.move(-self.player.x_speed / 10, -self.player.y_speed / 10)
                collision = self.__update_enemies_movements()
                self.score += 1 * self.num_of_ladybugs

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                self.__handle_keys(pygame.key.get_pressed())
            if collision:
                result = Caption("Twój wynik: " + str(self.score), 50)
                result.x = (self.width-result.text.get_width())/2
                result.y = (self.height-result.text.get_height())/2
                start.y = result.y + result.text.get_height() + 10
                self.__remove_ladybugs()
                self.__reset_player((self.width-self.player.width)/2, int(self.height/3))
                self.__screen_update([result, start])
                game = self.__get_space()
        pygame.quit()

    def __screen_update(self, added_captions=None):
        if added_captions is None:
            added_captions = []
        self.__screen.fill((0, 0, 0))
        self.__screen.blit(self.player.img, (self.player.x, self.player.y))
        for ladybug in self.ladybugs:
            self.__screen.blit(ladybug.img, (ladybug.x, ladybug.y))
        self.caption = Caption(str(self.score), 20)
        self.__screen.blit(self.caption.text, (10, 10))
        if len(added_captions) > 0:
            for caption in added_captions:
                self.__screen.blit(caption.text, (caption.x, caption.y))
        pygame.display.update()

    def __update_enemies_movements(self):
        for ladybug in self.ladybugs:
            if self.player.collides_with(ladybug):
                return True
            x_dir = random.choice((-1, 1))
            y_dir = random.choice((-1, 1))
            ladybug.move(x_dir * random.randint(1, 5) / 25, y_dir * random.randint(1, 5) / 25)
        return False

    def __handle_keys(self, keys):
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.player.move(0, -config.player_movespeed)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.player.move(0, config.player_movespeed)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.player.move(-config.player_movespeed, 0)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.player.move(config.player_movespeed, 0)

    def __remove_ladybugs(self):
        self.ladybugs.clear()

    def __reset_player(self, x_pos=0, y_pos=0):
        if not x_pos or not y_pos:
            self.player = Player((self.width - 30) / 2, (self.height - 30) / 2, 0, 0)
        else:
            self.player.x = x_pos
            self.player.y = y_pos

    def __get_space(self, space=True):
        while space:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        space = False
                    if event.key == pygame.K_ESCAPE:
                        return False
        return True

    class Menu:  # MENU HANDLER
        def __init__(self, width, height):
            self.__screen = pygame.display.set_mode((width, height))
            self.logo = pygame.image.load(os.path.join('Objects/imgs/ladybug-logo.png'))
            self.logo = pygame.transform.scale(self.logo, (300, 300))
            self.captions = [Caption("QUIT", 50, config.colors.get("Grey")),
                             Caption("START", 50, config.colors.get("White"))]
            self.width = width
            self.height = height
            self.selected = 1

        def run(self):
            pygame.time.wait(300)
            run = False
            while not run:
                self.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.time.wait(500)
                        return False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                            if self.selected == 0:
                                self.selected = len(self.captions)-1
                            else:
                                self.selected -= 1
                            self.captions[self.selected].change_color(config.colors.get("White"))
                        if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                            if self.selected == len(self.captions)-1:
                                self.selected = 0
                            else:
                                self.selected += 1
                            self.captions[self.selected].change_color(config.colors.get("White"))
                        if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            return self.selected

        def update(self):
            self.__screen.fill((0, 0, 0))
            self.__screen.blit(self.logo, ((self.width - 300) / 2, (self.height - 300) / 2))
            x = int(config.window_width/2)
            x_pos = x
            self.grey_captions_except(self.selected)
            for caption in self.captions:
                self.__screen.blit(caption.text, (x_pos-int(config.window_width/3), caption.size))
                x_pos += x
            pygame.display.update()

        def grey_captions_except(self, pos):
            for i in range(len(self.captions)):
                if i != pos:
                    self.captions[i].change_color()
