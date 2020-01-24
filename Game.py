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
from Music import Music

icon = pygame.image.load(os.path.join('ladybug.ico'))
logo = pygame.image.load(os.path.join('Objects/imgs/ladybug-logo.png'))


class Game(object):

    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.__set_screen_up()
        self.ladybugs = []
        self.player = Player((self.width - 30) / 2, (self.height - 30) / 2, 0, 0)
        self.FPS = config.fps
        self.clock = pygame.time.Clock()
        self.highscores = File(config.highscores_filename)
        self.mixer = Music('Objects/music/MoonlightSonata.mp3')

    def run(self):
        run = True
        while run:
            menu = self.Menu(self.width, self.height, self.__screen, self.mixer)
            self.mixer.play_from(-1, 360)
            run = menu.run()
            if run == 1:
                self.mixer.play_from(-1, 1)
                menu.open_highscores()
            elif run == 2:
                self.mixer.play_from(-1, 486)
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
                    self.__set_difficulty(config.difficulty)
                    self.__reset_player()
                    while run and not collision:
                        self.__screen_update()
                        self.clock.tick(self.FPS)
                        self.player.move(-self.player.x_speed / 10, -self.player.y_speed / 10)
                        collision = self.__update_enemies_movements()
                        self.player.score += config.difficulty
                        pygame.event.get()
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
        for i in range(num_of_ladybugs):
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
        self.highscores.data[i] = Score(self.player.name, self.player.score)
        while i > 0 and self.highscores.data[i] > self.highscores.data[i-1]:
            temp = self.highscores.data[i]
            self.highscores.data[i] = self.highscores.data[i-1]
            i -= 1
            self.highscores.data[i] = temp
        self.highscores.save()

    def __set_default_highscores(self):
        self.highscores.open()
        default_points = 100000
        highscores = []
        for i in range(10):
            highscores.append(Score(config.player_name, default_points))
            default_points -= 10000
        self.highscores.data = highscores
        self.highscores.save()

    def __set_screen_up(self):
        pygame.init()
        pygame.display.set_icon(icon)
        pygame.display.set_caption('Ladybug v1.1')
        self.__screen = pygame.display.set_mode((self.width, self.height))

    class Menu:  ############# MENU HANDLER #################
        def __init__(self, width, height, screen, mixer):
            self.__screen = screen
            self.logo = logo
            self.buttons = Buttons([[Caption("QUIT", 30, config.colors.get("Grey")),
                                    Caption("HIGHSCORES", 30, config.colors.get("Grey")),
                                    Caption("START", 30)],
                                    [Caption("PLAYER NAME: ", 30, config.colors.get("Grey")),
                                    Caption(config.player_name, 30, config.colors.get("Grey"))],
                                    [Caption("DIFFICULTY: ", 30, config.colors.get("Grey")),
                                    Caption(str(config.difficulty), 30, config.colors.get("Grey"))],
                                    [Caption("MUSIC: ON", 30, config.colors.get("Grey"))]])
            self.width = width
            self.height = height
            self.selection = Caption("QUIT")
            self.mixer = mixer

        def run(self):
            run = True
            while run:
                self.selection = self.buttons.handle_events()
                if self.selection is not None:
                    if self.selection == Caption("QUIT"):
                        return 0
                    elif self.selection == Caption("HIGHSCORES"):
                        return 1
                    elif self.selection == Caption("START"):
                        return 2
                    elif self.selection == Caption("PLAYER NAME: ") or self.selection == self.buttons.buttons[1][1]:
                        self.selection = self.buttons.buttons[1][1]
                        self.buttons.row = 1
                        self.buttons.col = 1
                        self.__get_playername()
                        # let the user type in the name
                    elif self.selection == Caption("DIFFICULTY: ") or self.selection == self.buttons.buttons[2][1]:
                        self.selection = self.buttons.buttons[2][1]
                        self.buttons.row = 2
                        self.buttons.col = 1
                        self.__get_difficulty()
                        # let the user change difficulty
                    elif self.selection == Caption("MUSIC: ON") or Caption("MUSIC: OFF"):
                        if self.mixer.is_on():
                            self.buttons.buttons[3][0] = Caption("MUSIC: OFF", 30)
                        else:
                            self.buttons.buttons[3][0] = Caption("MUSIC: ON", 30)
                        self.mixer.change_mode()
                self.update()
            return self.selection


        def update(self):
            self.__screen.fill((0, 0, 0))
            self.__screen.blit(self.logo, ((self.width-self.logo.get_width())/2, self.height-self.logo.get_height()-50))
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

        def __get_playername(self):
            player_name = ""
            run = True
            while run:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            if len(player_name):
                                player_name = player_name[:-1]
                        elif event.key == pygame.K_ESCAPE:
                            player_name = config.player_name
                            self.buttons.buttons[1][1] = Caption(player_name, 30)
                            run = False
                        elif event.key == pygame.K_RETURN:
                            config.player_name = player_name
                            run = False
                        elif len(player_name) < 16:
                            player_name += event.unicode
                self.buttons.buttons[1][1] = Caption(player_name, 30)
                self.update()
            self.selection = self.buttons.buttons[1][0]
            self.buttons.row = 1
            self.buttons.col = 0

        def __get_difficulty(self):
            difficulty = config.difficulty
            run = True
            while run:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_w or event.key == pygame.K_UP:
                            if difficulty < config.max_level:
                                difficulty += 1
                        elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                            if difficulty > config.min_level:
                                difficulty -= 1
                        elif event.key == pygame.K_ESCAPE:
                            difficulty = config.difficulty
                            self.buttons.buttons[2][1] = Caption(config.difficulty, 30)
                            run = False
                        elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                            config.difficulty = difficulty
                            run = False
                self.buttons.buttons[2][1] = Caption(difficulty, 30)
                self.update()
            self.selection = self.buttons.buttons[2][0]
            self.buttons.row = 2
            self.buttons.col = 0
