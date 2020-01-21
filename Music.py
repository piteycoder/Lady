import pygame


class Music:
    def __init__(self, filepath):
        pygame.mixer_music.load(filepath)
        pygame.mixer_music.set_volume(1)
        self.__mode = 1

    def play_from(self, loops, timestamp):
        pygame.mixer_music.rewind()
        pygame.mixer_music.play(loops, timestamp)

    def is_on(self):
        return self.__mode

    def change_mode(self):
        if self.__mode == True:
            pygame.mixer_music.set_volume(0)
            self.__mode = False
        else:
            pygame.mixer_music.set_volume(1)
            self.__mode = True
