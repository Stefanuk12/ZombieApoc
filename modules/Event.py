# Dependencies
from typing import Callable, List
from modules.Game import Game

# A base event
class Event:
    # The conditions needed to trigger this event
    conditions = ["Zombie"] * 2
    result: Callable

    # Constructor
    def __init__(self, conditions: List[str], result: Callable[[Game], bool]):
        self.conditions = conditions
        self.result = result