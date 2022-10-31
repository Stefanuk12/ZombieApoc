# Dependencies
from typing import Callable
from modules.Event import Event
from random import randint
from modules.Game import Events, Game
from modules.Menu import Menu

# Decorator for creating events
def event(func: Callable):
    # Make sure we have a valid function name
    funcNameSplit = func.__name__.split("_")
    if (len(funcNameSplit) != 2):
        raise(NameError("Invalid function name. Must have two conditions seperated by an underscore"))

    # Creating the event
    Events.append(Event(funcNameSplit, func))

    # Return
    return func

# Bug. The state of the ammoMenu is retained. If you have many zombie apocs, and attempt to shoot in each one, the menu items are the same + more from last time. (line 43)
@event
def Zombie_Zombie(game: Game):
    # Intro - calculate the number of zombies
    print("Zombie Apocalypse!")
    zombies = randint(1, 4)
    usedAmmo = zombies if (game.ammo >= zombies) else game.ammo
    print(f"{zombies} zombies have spawned...")

    # Get user input on what to do
    menu = Menu("What do we do?", None, [
        "Dispatch the trusty bat 'Lucille'"   
    ])

    #
    if (game.fred):
        menu.Add("Sacrifice Fred")

    # We have ammo, attempt to use it
    if (usedAmmo > 0):
        ammoMenus = Menu("Shoot the zombies", menu)
        for i in range(usedAmmo):
            #print(ammoMenus.children)
            ammoMenus.Add(f"Shoot {i + 1} zombies")

    # Ask the user on what to do
    response, responsemenu = menu.Start()

    # rip fred
    if (response == "Sacrifice Fred"):
        game.fred = None
        zombies = 0
        return True

    # Shooting the zombies
    if (response.find("Shoot") != -1):
        # Get the number of zombies to shoot
        ammoUse = [int(s) for s in response.split() if s.isdigit()][0]
        zombies -= ammoUse
        game.ammo -= ammoUse

    # There are no zombies left
    if (zombies <= 0):
        print("Phew. They're all dead.")
        return True

    # Velma
    if (response == "Dispatch the trusty bat 'Lucille'" or zombies > 0):
        print("Velma, go!")

        lastRoll = 0
        while True:
            # For each zombie
            for i in range(zombies):
                roll = randint(1, 5)
                lastRoll = roll

                # odd (successful)
                if (roll % 2 != 0):
                    zombies -= 1
                    print("Take the bat zombie!")
                else:
                    print("Ah! I missed!")

                # double
                if (lastRoll == 1 and roll == 1):
                    zombies += 2
                    print("Two more zombies!?")

            # Check if there are no more zombies left
            if (zombies <= 0):
                break

    # There are no zombies left
    if (zombies <= 0):
        print("Phew. They're all dead.")
        return True
    else:
        return False # should not happen