import config


class Object:
    def __init__(self, x, y, x_speed, y_speed, width, height):
        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.width = width
        self.height = height

    def move(self, x_speed, y_speed):
        self.x_speed += x_speed
        if self.x + self.x_speed <= 0:
            self.x = 0
            self.x_speed = -(self.x_speed/4)
        if self.x + self.x_speed + self.width >= config.window_width:
            self.x = config.window_width - self.width
            self.x_speed = -(self.x_speed/4)
        self.x += self.x_speed

        self.y_speed += y_speed
        if self.y + self.y_speed + self.height >= config.window_height:
            self.y = config.window_height - self.height
            self.y_speed = -(self.y_speed/4)
        if self.y + self.y_speed <= 0:
            self.y = 0
            self.y_speed = -(self.y_speed/4)
        self.y += self.y_speed

    def collides(self, other):
        return False
