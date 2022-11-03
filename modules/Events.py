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

# Nothing events.
@event
def Zombie_Nothing(game: Game):
    print("You spot a zombie in the far distance... You continue on.")
@event
def Ammo_Nothing(game: Game):
    print("While exploring you found some ammo, shame that they are just casings. I wonder what happened here...")
@event
def Food_Nothing(game: Game):
    print("There was a slice of cheese on the floor. It smelt... fresh?")
@event
def Survivor_Nothing(game: Game):
    print("You're getting lonely... You waved to your imaginary friend.")

# Bug. The state of the ammoMenu is retained. If you have many zombie apocs, and attempt to shoot in each one, the menu items are the same + more from last time. (line 43). To do: Check if Velma is alive, if not sacrifice a survivor or take damage 
@event
def Zombie_Zombie(game: Game):
    # Intro - calculate the number of zombies
    print("""
    ZzZZzzzZOMBIE APOCALYPSE!!                       
                           \                     
                                .....            
                               C C  /            
                              /<   /             
               ___ __________/_#__=o             
              /(- /(\_\________   \              
              \ ) \ )_      \o     \             
              /|\ /|\       |'     |             
                            |     _|             
                            /o   __\             
                           / '     |             
                          / /      |             
                         /_/\______|             
                        (   _(    <              
                         \    \    \             
                          \    \    |            
                           \____\____\           
                           ____\_\__\_\          
                         /`   /`     o\          
                         |___ |_______|.. .
    """)
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
        print("No, Fred. Don't do it! NOOOOOOOOOOOOOOOOOO.")
        print("All zombies are dead.")
        return True

    # Shooting the zombies
    if (response.find("Shoot") != -1):
        # Get the number of zombies to shoot
        ammoUse = [int(s) for s in response.split() if s.isdigit()][0]
        zombies -= ammoUse
        game.ammo -= ammoUse
        print("Ammo casings litter the floor...")

    # There are no zombies left
    if (zombies <= 0):
        print("Phew. They're all dead.")
        return True

    # Velma
    if (response == "Dispatch the trusty bat 'Lucille'" or zombies > 0):
        print("Velma, go!")

        lastRoll = 0
        while (game.hp > 0):
            # For each zombie
            for i in range(zombies):
                # Check if died
                if (game.hp <= 0):
                    break

                # Roll
                roll = randint(1, 10)
                lastRoll = roll

                # Successful hit
                if (roll <= 8):
                    zombies -= 1
                    print("Take the bat zombie!")
                else:
                    print("Ah! I missed! OWWW")
                    game.hp -= 1

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
        return False # should not happen unless died

#
@event
def Zombie_Ammo(game: Game):
    # Intro
    print("""
            ___
        ,-""___""-.
       .;""'| |`"":.
       || | | | | ||
       ||_|_|_|_|_||
      //          /|
     /__         //|
 ,-""___""-.    //||
.;""'| |`"":.  //
||/| | | | || //
||_|_|_|_|_||//
||_________||/
||         ||
''         ''  
""")
    print("You come across a zombie... It seems to be unconcious on some ammo...")

    # Ask the user on what to do
    menu = Menu("What will you do?", None, [
        "Attempt to steal the ammo",
        "Walk past quietly"
    ])
    response, _ = menu.Start(None, True)

    # Check if zombie wakes up
    zombieWakeChance = 8 if response == "Walk past quietly" else 5
    d10 = randint(1, 10)
    if (d10 <= zombieWakeChance):
        # Check if we selected to steal the ammo
        if (response == "Attempt to steal the ammo"):
            # Add the ammo
            stolenAmmo = d10 // 3
            game.ammo += d10 // 3
            print("Come on, come on, come on... Just, move, this... yes!")
            print(f"You have successfully stolen {stolenAmmo} from the zombie.")

        #
        print("You walk quietly past the zombie")
        return False

    # Zombie woke up, uh oh
    print("You walk past, but trip over a wire on the floor. The zombie wakes and sees you...")
    zombieMenu = Menu("What will you do?", None, [
        "" # implement zombie apoc logic here
    ])