class Survivor:
    type: str = "Basic" # The type of survivor
    runningAway = -1 # Whether a survivor is going to run away in a certain amount of days
    humanView: str = "A basic survivor that only eats your food up."
    icon: str = "( ͡° ͜ʖ ͡°)"

    # Constructor
    def __init__(self, type: str = None, runningAway: int = None):
        self.type = self.type or type
        self.runningAway = self.runningAway or runningAway

    # The cost of a survivor per day, i.e. -1 food a day
    def cost(self, game):
        # Make sure there is food
        if (game.food > 0):
            game.food -= 1
            game.runningAway = -1
        else:
            # Set running away, if not
            if (game.runningAway == -1):
                game.runningAway = 3
            else:
                game.runningAway -= 1

    # Any benefits of holding the survivor, i.e. a medic - +1hp per day
    def benefit(self, game):
        pass

# Survivor types
class Medic(Survivor):
    type: str = "Medic"
    humanView: str = "A medic that heals you one HP per round at the expense of one food."
    icon: str = """
......
:.  .:
.'  '.
|    |
|    |
`----'
"""

    def benefit(self, game):
        game.hp += 1