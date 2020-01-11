class Score:
    def __init__(self, name, score):
        self.player_name = name
        self.score = score

    def __gt__(self, other):
        return self.score > other.score
