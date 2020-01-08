class File:
    def __init__(self, path, mode='rb'):
        self.path = path
        self.mode = mode
        self.data = None

    def open(self):
        with open(self.path, self.mode) as file:
            data = file.read(64)

    def save(self):
        pass

    def get_data(self):
        pass