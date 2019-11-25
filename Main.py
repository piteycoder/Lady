from Game import Game
import config

game = Game(config.window_width, config.window_height)
game.set_difficulty(20)
game.run()
