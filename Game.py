import random
import pygame
import config
import os

from Objects.Ladybug import Ladybug
from Objects.Player import Player
from Objects.Caption import Caption
from File import File
from Score import Score
from Buttons import Buttons


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
        self.highscores = File(config.highscores_filename)
        self.caption = Caption("text", 20)

    def run(self):
        run = True
        while run:
            menu = self.Menu(self.width, self.height)
            run = menu.run()
            if run == 1:
                menu.open_highscores()
            elif run == 2:
                start = Caption("WCIŚNIJ SPACJĘ ABY ROZPOCZĄĆ", 30, config.colors.get("White"))
                start.x = (self.width - start.text.get_width()) / 2
                start.y = int(self.height * 0.7)
                self.__screen_update([start])
                game = self.__get_space()
                while game:
                    run = True
                    collision = False
                    self.player.score = 0
                    start.y = int(self.height*0.7)
                    self.__set_difficulty()
                    self.__reset_player()
                    while run and not collision:
                        self.__screen_update()
                        self.clock.tick(self.FPS)

                        self.player.move(-self.player.x_speed / 10, -self.player.y_speed / 10)
                        collision = self.__update_enemies_movements()
                        self.player.score += self.num_of_ladybugs

                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                run = False
                            elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:
                                    run = False

                        self.__handle_keys(pygame.key.get_pressed())
                    if collision:
                        result = Caption("Twój wynik: " + str(self.player.score), 50)
                        result.x = int((self.width-result.text.get_width())/2)
                        result.y = int((self.height-result.text.get_height())/2)
                        start.y = result.y + result.text.get_height() + 10
                        self.__remove_ladybugs()
                        self.__reset_player((self.width-self.player.width)/2, int(self.height/3))
                        self.__screen_update([result, start])
                        self.__update_highscores()
                        game = self.__get_space()

        pygame.quit()

    def __set_difficulty(self, num_of_ladybugs=config.default_level):
        self.num_of_ladybugs = num_of_ladybugs
        for i in range(self.num_of_ladybugs):
            x_pos = random.choice((random.randint(0, self.width / 2 - 60),
                                   random.randint(self.width / 2 + 30, self.width - 30)))
            y_pos = random.choice((random.randint(0, self.height / 2 - 60),
                                   random.randint(self.height / 2 + 30, self.height - 30)))
            self.ladybugs.append(Ladybug(x_pos, y_pos, random.randint(1, 5) / 1000, random.randint(1, 5) / 1000))

    def __screen_update(self, added_captions=None):
        if added_captions is None:
            added_captions = []
        self.__screen.fill((0, 0, 0))
        self.__screen.blit(self.player.img, (self.player.x, self.player.y))
        for ladybug in self.ladybugs:
            self.__screen.blit(ladybug.img, (ladybug.x, ladybug.y))
        self.caption = Caption(str(self.player.score), 20)
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

    def __update_highscores(self):
        self.highscores.open()
        i = len(self.highscores.data)-1
        if self.player.score <= self.highscores.data[i].score:
            return
        print("Score to be saved: " + str(self.player.score))
        self.highscores.data[i] = Score(self.player.name, self.player.score)
        print("Score saved: " + str(self.highscores.data[i].score))
        while i > 0 and self.highscores.data[i] > self.highscores.data[i-1]:
            temp = self.highscores.data[i]
            self.highscores.data[i] = self.highscores.data[i-1]
            i -= 1
            self.highscores.data[i] = temp
        self.highscores.save()

    def __set_default_highscores(self):
        default_points = 100000
        highscores = []
        for i in range(10):
            highscores.append(Score(config.player_name, default_points))
            default_points -= 10000
        return highscores

    class Menu:  ############# MENU HANDLER #################
        def __init__(self, width, height):
            self.__screen = pygame.display.set_mode((width, height))
            self.logo = pygame.image.load(os.path.join('Objects/imgs/ladybug-logo.png'))
            self.logo = pygame.transform.scale(self.logo, (300, 300))
            self.buttons = Buttons([[Caption("QUIT", 30, config.colors.get("Grey")),
                            Caption("HIGHSCORES", 30, config.colors.get("Grey")),
                             Caption("START", 30)],
                             [Caption("Player name: ", 30, config.colors.get("Grey")),
                              Caption("", 30, config.colors.get("Grey"))],
                             [Caption("Set difficulty: ", 30, config.colors.get("Grey")),
                              Caption(str(config.default_level), 30, config.colors.get("Grey"))]])
            self.width = width
            self.height = height
            self.selection = Caption("QUIT")

        def run(self):
            run = True
            while run >= 0:
                self.update()
                run = self.buttons.handle_events()
            if run < 0:
                return run
            return self.selection


        def update(self):
            self.__screen.fill((0, 0, 0))
            self.__screen.blit(self.logo, ((self.width - (self.logo.get_width()+50)), (self.height - 300) / 2))
            self.buttons.update(self.__screen)
            pygame.display.update()

        def open_highscores(self):
            run = True
            highscores = File(config.highscores_filename)
            highscores.open()
            title = Caption("HIGHSCORE TABLE", 30)
            x_pos = int((self.width - title.get_width()) / 2)
            while run:
                y_pos = 40
                self.__screen.fill((0, 0, 0))
                self.__screen.blit(title.text, (x_pos, y_pos))
                y_pos += title.get_height()
                for score in highscores.data:
                    player = (Caption(score.player_name, 20), Caption(": ", 20), Caption(score.score, 20))
                    y_pos += int((player[0].get_height()/2)*3)
                    for caption in player:
                        self.__screen.blit(caption.text, (x_pos, y_pos))
                        x_pos += caption.get_width()
                    x_pos = int((self.width - title.get_width()) / 2)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            return False

                pygame.display.update()
