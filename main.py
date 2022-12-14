# Dependencies
from modules.Game import Game
from modules.Survivor import Survivor, Medic
import modules.Events # Force the events to run
from modules.Utils import time_input
import os

# Creating the game object
game = Game()
testing = True

# Starts the game
if (not testing):
    game.Start()
    os._exit(0)

# TESTS
game.survivors.append(Survivor())
game.survivors.append(Medic())
game.survivors.append(Survivor())

# game.StartRound(1, 1)
# game.StartRound(1, 2)
# game.StartRound(1, 4)
# game.StartRound(1, 6)
# game.StartRound(2, 2)
# game.StartRound(2, 4)
# game.StartRound(2, 6)
# game.StartRound(4, 4)
game.StartRound(6, 6)

# TESTS - nothing events
# game.StartRound(1, 5)
# game.StartRound(2, 5)
# game.StartRound(4, 5)
# game.StartRound(6, 5)

# game.StartRound(5, 1)
# game.StartRound(5, 2)
# game.StartRound(5, 4)
# game.StartRound(5, 6)