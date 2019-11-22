class Object:
    def __init__(self, x, y, x_speed, y_speed, width, height):
        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.width = width
        self.height = height

    def move(self, x_speed, y_speed):
        width = 800
        height = 600
        self.x_speed += x_speed
        self.y_speed += y_speed
        if self.x + self.x_speed + self.width >= width:
            self.x = width - self.width
            self.x_speed *= -1
        elif self.x + self.x_speed <= 0:
            self.x = 0
            self.x_speed *= -1
        if self.y + self.y_speed <= 0:
            self.y = 0
            self.y_speed *= -1
        elif self.y + self.y_speed + self.height >= height:
            self.y = height - self.height
            self.y_speed *= -1
