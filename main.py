# Dependencies
from modules.Game import Game
import modules.Events # Force the events to run
import os

# Creating the game object
game = Game()
testing = True

# Starts the game
if (not testing):
    game.Start()
    os._exit(0)

# TESTS
game.StartRound(1, 1)

# TESTS - nothing events
game.StartRound(1, 5)
game.StartRound(2, 5)
game.StartRound(4, 5)
game.StartRound(6, 5)