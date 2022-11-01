# Dependencies
from random import randint
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
"RisingSun": """
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
------------
Dogs: {dogs}
Ammo: {ammo}
Survivors: {survivors}
"""
}

#
class Game:
    # Vars
    round = 0
    dogs = 1
    ammo = 3

    # Characters
    fred = True
    velma = True
    persons = 0

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
        risingSun = StringFormatting["RisingSun"].center(terminalSize.columns)
        print(risingSun)
        
        # Work out which characters will be joining
        characters = []
        if (self.fred):
            characters.append("Fred")
        if (self.velma):
            characters.append("Velma")
        charactersJoining = ", ".join(characters) if len(characters) != 0 else "No"        

        # Print stats
        logFormatted = StringFormatting["RoundStats"].format(round=self.round, characters=charactersJoining, dogs=self.dogs, ammo=self.ammo, survivors=self.persons)
        print(logFormatted.center(terminalSize.columns))

        # Seperator
        print(">---<\n")

    #
    def StartRound(self, d1=None, d2=None):
        # Check the rounds
        if (self.round > 100):
            print("You have survived. Congrats!")
            return True

        # Check if we died
        if (self.fred == False and self.velma == False and self.persons == 0):
            print("You have died!")
            return True
    
        # Intro
        self.round += 1
        self.PrintRoundInformation()

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

    # Actually starts the entire game
    def Start(self):
        while (self.StartRound() == False):
            pass