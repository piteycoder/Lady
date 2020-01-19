import pygame
import config


class Buttons:
    def __init__(self, button_list):
        self.buttons = button_list
        self.row = 0
        self.col = 0

    def get_selected(self):
        return self.buttons[self.row, self.col]

    def add_to_row(self, row=0, button=None):
        self.buttons[row].append(button)

    def clear(self):
        self.buttons.clear()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return self.buttons[0][0]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    self.__handle_left_move()
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.__handle_right_move()
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.__handle_up_move()
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.__handle_down_move()
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    return self.buttons[self.row][self.col]
        return None

    def update(self, screen):
        y_pos = 30
        for buttons in self.buttons:
            x_pos = 30
            for button in buttons:
                if button != self.buttons[self.row][self.col]:
                    button.change_color()
                else:
                    button.change_color(config.colors.get("White"))
                screen.blit(button.text, (x_pos, y_pos))
                x_pos += button.text.get_width() + 30
            y_pos += 60

    def __handle_left_move(self):
        if self.col > 0:
            self.col -= 1

    def __handle_right_move(self):
        if self.col+1 < len(self.buttons[self.row]):
            self.col += 1

    def __handle_up_move(self):
        if self.row > 0:
            self.row -= 1
            self.col = 0

    def __handle_down_move(self):
        if self.row+1 < len(self.buttons):
            self.row += 1
            self.col = 0
