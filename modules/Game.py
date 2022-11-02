# Dependencies
from random import randint
from modules.Survivor import Survivor
from typing import List
from modules.Menu import Menu
import os

# Holds all of the game events
Events = []

# Clears the console
def clear():
    # Windows
    if (os.name == "nt"):
        os.system("cls")
    else: # others
        os.system("clear")

# Holds some ASCII art and other formatting
StringFormatting = {
"RisingSun": 
"""
                  \       /            _\/_
                   .-'-.              //o\  _\/_
_  ___  __  _ --_ /     \ _--_ __  __ _ | __/o\\ _
=-=-_=-=-_=-=_=-_= -=======- = =-=_=-=_,-'|"'""-|-,_ 
=- _=-=-_=- _=-= _--=====- _=-=_-_,-"          |
=- =- =-= =- = -  -===- -= - ."
""",
"RoundStats": """
Round {round} has started.
{characters} will be joining you...

Statistics:
-------------
Health ♥: {health}
Food 🥫: {food}
Dogs ▼・ᴥ・▼: {dogs}
Ammo ⁍⁍⁍: {ammo}
Survivors 👤: {survivors}
"""
}

# Centers a string, adds support for multiline ones
def centerString(string: str, columns: int):
    return "\n".join(line.center(columns)  for line in string.split("\n"))

#
class Game:
    # Vars
    round = 0
    dogs = 1
    ammo = 3
    hp = 10
    food = 30

    # Characters
    fred = True
    velma = True
    survivors: List[Survivor] = []

    # Dice lookup
    diceLookup = [
        "YOU SHOULD NOT BE SEEING THIS. BUG ALERT", # To make the array 1-based
        "Zombie",
        "Ammo",
        "Zombie",
        "Food",
        "Nothing",
        "Survivor"
    ]

    # Print out round information
    def PrintRoundInformation(self):
        # Clear the output so far
        clear()

        # ASCII art
        terminalSize = os.get_terminal_size()
        risingSun = centerString(StringFormatting["RisingSun"], terminalSize.columns)
        print(risingSun)
        
        # Work out which characters will be joining
        characters = []
        if (self.fred):
            characters.append("Fred")
        if (self.velma):
            characters.append("Velma")
        charactersJoining = ", ".join(characters) if len(characters) != 0 else "No"        

        # Print stats
        logFormatted = StringFormatting["RoundStats"].format(round=self.round, characters=charactersJoining, health=self.hp, food=self.food, dogs=self.dogs, ammo=self.ammo, survivors=len(self.survivors))
        print(centerString(logFormatted, terminalSize.columns))

        # Seperator
        print(">---<".center(terminalSize.columns))
        print()

    # Performs the dice roll
    def DiceRoll(self, d1=None, d2=None):
        # Rolling dice
        sidedDice = len(self.diceLookup) - 1
        d1 = d1 or randint(1, sidedDice)
        d2 = d2 or randint(1, sidedDice)

        # Announce roll
        print(f"A {d1} ({self.diceLookup[d1]}) and a {d2} ({self.diceLookup[d2]}) has been rolled...")

        # Possible reroll
        while (self.dogs >= 1):
            # Creating the re roll menu
            menu = Menu(f"Do you wish to reroll, you have {self.dogs} dog(s)?", None, [
                "No"
            ])
            Menu("Yes", menu, [
                "Reroll dice 1",
                "Reroll dice 2"
            ])

            # Get response
            response, _ = menu.Start(None, True)

            # No
            if (response == "No"):
                break

            # Reroll
            if (response == "Reroll dice 1"):
                d1 = randint(1, 6)

                # Check if zombie
                if (self.diceLookup[d1] == "Zombie"):
                    print(f"You have rerolled a Zombie ({d1}), you have lost one dog!")
                    self.dogs -= 1
                else:
                    print(f"You have rerolled a {d1}")
            elif (response == "Reroll dice 2"):
                d2 = randint(1, 6)

                # Check if zombie
                if (self.diceLookup[d2] == "Zombie"):
                    print(f"You have rerolled a Zombie ({d2}), you have lost one dog!")
                    self.dogs -= 1
                else:
                    print(f"You have rerolled a {d2}")

        # Figure out the event
        conditions = [self.diceLookup[d1], self.diceLookup[d2]]
        event = None
        try:
            filtered = filter(lambda x: x.conditions == conditions, Events)
            event = next(filtered)
        except:
            print("Nothing happened...")
            input("Press enter to continue...")
            return False

        # Run the event
        event.result(self)
        input("Press enter to continue...")
        return False
    
    #
    def StartRound(self, d1=None, d2=None):
        # Check the rounds
        if (self.round > 100):
            print("GAME END: You have survived. Congrats!")
            return True

        # Check if we died. Prints repeatedly on test mode. Force exit?
        if (self.hp <= 0):
            print("ugh... ow. i think it's time... time to close my eyes...")
            print("GAME END: You have died.")
            return True
    
        # Next round
        self.round += 1

        # Loop through each survivor
        for i, survivor in enumerate(self.survivors):
            # Run the cost
            survivor.cost(self)

            # Survivor "died"
            if (survivor.runningAway == 0):
                print("You have lost a survivor during the night...")
                self.survivors.pop(i)
            else:
                survivor.benefit(self)
                print("ran benefit")

        # Output the info
        self.PrintRoundInformation()

        # Will only break out via return when the day is started
        terminalSize = os.get_terminal_size()
        while True:
            # User input
            menu = Menu("Select one", None, [
                "Start the day...",
                "View statistics"
            ])

            # Adding extra 
            if (len(self.survivors) > 0):
                menu.Add("See your survivors")

            # Getting repsonse
            menuresponse, _ = menu.Start(None, True)
            clear()

            # Doing it
            if (menuresponse == "Start the day..."):
                # Roll the dice
                return self.DiceRoll(d1, d2)
            elif (menuresponse == "View statistics"):
                self.PrintRoundInformation()
            elif (menuresponse == "See your survivors"):
                # Loop through each survivor
                for survivor in self.survivors:
                    # Print their details
                    print(centerString(survivor.icon, terminalSize.columns))
                    print(survivor.type.center(terminalSize.columns))
                    print(survivor.humanView.center(terminalSize.columns) + "\n\n")

                    # Prompt
                    input("Press any key to view the next...".center(terminalSize.columns))
                    clear()

    # Actually starts the entire game
    def Start(self):
        while (self.StartRound() == False):
            pass