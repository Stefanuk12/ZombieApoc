# Dependencies
from typing import Callable
from modules.Event import Event
from random import randint, choice
from modules.Game import Events, Game
from modules.Menu import Menu
from modules.Survivor import Survivor, Medic
from modules.Utils import s_print, colours, time_input
import string

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
def Nothing_Nothing(game: Game):
    s_print("The wind wails, and the skies cry... You put up your ragged hood and walk on...")
@event
def Zombie_Nothing(game: Game):
    s_print("You spot a zombie in the far distance... You continue on.")
@event
def Ammo_Nothing(game: Game):
    s_print("While exploring you found some ammo, shame that they are just casings. I wonder what happened here...")
@event
def Food_Nothing(game: Game):
    s_print(f"{colours.fg.lightblue}There was a slice of cheese on the floor. It smelt... fresh?", 0.5)
@event
def Survivor_Nothing(game: Game):
    s_print(f"{colours.fg.blue}You're getting lonely... You waved to your imaginary friend.", 1.5)

# Zombie events
@event

# Zombie events
# Bug. The state of the ammoMenu is retained. If you have many zombie apocs, and attempt to shoot in each one, the menu items are the same + more from last time. (line 43). To do: Check if Velma is alive, if not sacrifice a survivor or take damage 
def Zombie_Zombie(game: Game):
    # Intro - calculate the number of zombies
    print(f"""
    {colours.fg.green}ZzZZzzzZOMBIE APOCALYPSE!!{colours.reset}               
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
        s_print(f"{colours.fg.blue}No, Fred. Don't do it! NOOOOOOOOOOOOOOOOOO.")
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
        s_print(f"{colours.fg.blue}Phew. They're all dead.")
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
                    s_print(f"{colours.fg.blue}Take the bat, zombie!")
                    print(f"{colours.fg.lightgreen}-1 Zombie{colours.reset}")
                else:
                    s_print(f"{colours.fg.blue}Ah! I missed! OWWW")
                    print(f"{colours.fg.red}-1 Health{colours.reset}")
                    game.hp -= 1

                # double
                if (lastRoll == 1 and roll == 1):
                    zombies += 2
                    s_print(f"{colours.fg.blue}Two more zombies!?")
                    print(f"{colours.fg.red}+2 Zombies{colours.reset}")

            # Check if there are no more zombies left
            if (zombies <= 0):
                break

    # There are no zombies left
    if (zombies <= 0):
        print(f"{colours.fg.blue}Phew. They're all dead.{colours.reset}")
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
    s_print("You come across a zombie... It seems to be unconcious on some ammo...")

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
            stolenAmmo = 1 if stolenAmmo <= 0 else stolenAmmo
            game.ammo += d10 // 3
            s_print(f"{colours.fg.blue}Come on, come on, come on... Just, move, this... yes!")
            print(f"You have successfully stolen {stolenAmmo} ammo from the zombie.")
            print(f"{colours.fg.green}+ {stolenAmmo} Ammo{colours.reset}")
        #
        print("You walk quietly past the zombie.")
        return False

    # Zombie woke up, uh oh
    s_print("You walk past, but trip over a wire on the floor. The zombie wakes and sees you...")
    s_print("You didn't notice...")
    s_print("It starts to sneak upon you while you remain oblivious...")
    s_print(f"{colours.fg.blue}AHHH, OW!", 0.5)
    print("-1 Health")
    game.hp -= 1

#
@event
def Zombie_Food(game: Game):
    print("""
[_______________________________]
|===============================|
|   __                          |
|._/_.' _, ,__  ,_ /_ _  / /'   |
| / _  / / /// / // /(-'/ / /|  |
| \__)(_(_//(_/_/(_/(__(_(_/_/_ |
|            /                  |
|       C O N D E N S E D       |
|                               |
|            .-" "-.            |
|           /:`:..':\           |
|==========|.:::::..:|==========|
|           \::::::./           |
|            `-:::-'            |
|     ___                       |
|      |  _ ,_ _  _ -|- _       |
|      | (_)| | |(_| |_(_)      |
|                               |
|V( )V( )V(  S O U P  )V( )V( )V|
|----------           ----------|
'==============================='   
""")
    s_print(f"{colours.fg.green}Mmmm... Delicus fud...")
    s_print("You see a survivor? eating food, you approach to say hello...")
    s_print(f"{colours.fg.green}Hm? ARGGG, BRAINSSSS!")
    s_print(f"{colours.fg.blue}Uh oh. That's no survivor! RUN!!!")
    print("You barely escape, and managed to steal some food on the run.")
    s_print(f"{colours.fg.lightgreen}+1 Food")
    game.food += 1

#
@event
def Zombie_Survivor(game: Game):
    # Intro
    print("""
                (()))
               /|x x|
              /\( - )
      ___.-._/\/
     /=`_'-'-'/  !!
     |-{-_-_-}     !
     (-{-_-_-}    !
      \{_-_-_}   !
       }-_-_-}
       {-_|-_}
       {-_|_-}
       {_-|-_}
       {_-|-_} 
   ____%%@ @%%_______    
""")
    s_print("You find a zombie. He doesn't seem to be hostile... Freshly turned?")
    
    # Ask for input
    menu = Menu("Do you want to try and convert the zombie back?", None, [
        "Yes",
        "No"
    ])

    # Run
    response, _ = menu.Start()
    if (response == "No"):
        s_print("You quickly run past...")
        return False

    # Attempt to convert the zombie
    success = randint(1, 10) <= 4
    s_print(f"{colours.fg.blue}Ok lets see what we are working with here...")
    s_print(f"{colours.fg.blue}Add a dash of this...", 0.25)
    s_print(f"{colours.fg.blue}Add a dash of that...", 0.25)
    s_print(f"{colours.fg.blue}Turn around...", 0.4)
    s_print(f"{colours.fg.blue}Touch my toes...", 0.5)
    s_print(f"{colours.fg.blue}Aaaaand...")

    # Failed
    if (not success):
        s_print(f"{colours.fg.blue}Uh oh.")
        s_print(f"{colours.fg.green}BRAINS? BRAINS!!!")

        # Lose HP
        game.hp -= 1
        print(f"{colours.fg.red}-1 Health{colours.reset}")
        return False

    # Success
    medicSuccess = randint(1, 10) <= 8
    survivor = Medic() if medicSuccess else Survivor()
    s_print(f"The zombie successfully turned.")
    s_print(f"It seemed to be a {survivor.type} zombie in its past life...")
    print(f"{colours.fg.green}+1 {survivor.type}{colours.reset}")
    game.survivors.append(survivor)

# Ammo events
@event

# Ammo events
def Ammo_Ammo(game: Game):
    print("""
                           ______
        |\_______________ (_____\\______________
HH======#H###############H#######################
        ' ~""""""""""""""`##(_))#H\""''"Y########
                          ))    \#H\       `"Y###
                         "      }#H)    
""")
    ammoAmount = randint(3, 10)
    s_print("You came across an abandoned warehouse...")
    s_print("It held plentiful amounts of ammo.")
    print(f"{colours.fg.green}+ {ammoAmount} Ammo{colours.reset}")
    game.ammo += ammoAmount
    s_print("You see another survivor... He offers you a proposition")

    # Ask the user if they want to gamble their ammo
    menu = Menu(f"Will you gamble your {ammoAmount} ammo?", None, [
        "Yes",
        "No"
    ])
    response, _ = menu.Start()

    # They don't
    if (response == "No"):
        s_print("You back away slowly... Then start to run away.")
        s_print(f"{colours.fg.red}Where are you going?")
        return False

    # They do
    success = randint(1, 10) <= 3
    s_print("The survivor writes 3 numbers on a piece of paper... You attempt to guess at least one...")
    s_print(f"{colours.fg.blue}My guess is... 5")

    # Fail
    if (not success):
        s_print(f"{colours.fg.red}You are... incorrect.")
        s_print("You give the survivor their winnings, and walk away in defeat.")
        print(f"{colours.fg.red}- {ammoAmount} Ammo{colours.reset}")
        return False

    # Success
    s_print(f"{colours.fg.red}You are... correct! Lucky ba-")
    s_print("You take your winnings from the survivor.")
    s_print(f"{colours.fg.blue}Thank you very much.")
    s_print("You walk away with a smerk on your face.")
    game.ammo += ammoAmount

@event
def Ammo_Food(game: Game):
    # Intro
    giveUpAmount = randint(1, 3)
    s_print("While travelling, you found yourself in a predicament...")
    s_print(f"A survivor, operating a toll, demands you give up either {giveUpAmount} food or {giveUpAmount} ammo. Or else...")

    # Ask for user input
    menu = Menu("What will you give up?", None, [
        "Food",
        "Ammo"
    ])
    response, _ = menu.Start()

    # Dialog
    s_print(f"{colours.fg.red}Hurry up already, my time is valuable.")
    s_print(f"{colours.fg.blue}Fine, fine. Here.")
    print(f"{colours.fg.red}- {giveUpAmount} {response}{colours.reset}")
    s_print("The survivor knods, letting you pass")

    # Subtract
    if (response == "Food"):
        game.food -= giveUpAmount
    else:
        game.ammo -= giveUpAmount
@event
def Ammo_Survivor(game: Game):
    # Intro
    s_print("You see a survivor in the distance... They seem to be.. pregnant?")
    s_print(f"{colours.fg.red}Hello? Anybody there? Help me. Please.")
    s_print("You rush over, but remain cautious...")
    s_print(f"{colours.fg.blue}Hello? What's wrong?")
    s_print(f"{colours.fg.red}I... am so hungry. Please, give me food.")

    # Ask for user input
    menu = Menu("Will you give the survivor food?", None, [
        "Yes",
        "No"
    ])
    response, _ = menu.Start()

    # Yes
    if (response == "Yes"):
        s_print(f"{colours.fg.blue}Here. Are you okay?")
        s_print(f"{colours.fg.red}I'm a lot better now, thank you.")
        s_print("They scruffle through their ripped bag, looking for something...")
        s_print("You remain alert... Just in case.")
        s_print(f"{colours.fg.red}I don't have a lot but here.")
        print(f"{colours.fg.green}+1 Ammo{colours.reset}")
        game.ammo += 1
        s_print(f"{colours.fg.blue}Oh, thank you. You didn't have to.")
        s_print(f"{colours.fg.red}I know, but nothing is free in this world anymore...")
        s_print(f"{colours.fg.blue}I guess... I have to go. I hope you do well.")
        s_print("You walk away.")
        s_print(f"{colours.fg.red}You too.")
        s_print("You turn back, and give a smile, before then continuing to walk off.")
        return False

    # No
    s_print(f"{colours.fg.blue}I'm sorry, I can't.")
    s_print("You walk away nonchalantly.")
    s_print(f"{colours.fg.red}You vile person! Who would not help a pregnant lady?")
    s_print("She hits you in a fit of rage while you attempt to run away.")
    game.hp -= 1
    print(f"{colours.fg.red}-1 Health{colours.reset}")
    s_print("You run away, and while you do, you hear them shouting at you.")
    s_print(f"{colours.fg.red}I hope you rot and die.")
    s_print(f"{colours.fg.blue}Ow. My feelings. What's wrong with her?")
    s_print("You kept on running...")

# Food events
@event

# Food events
@event
def Food_Food(game: Game):
    # Introduction
    print("""
                            |\ /| /|_/|
                          |\||-|\||-/|/|
                           \\|\|//||///
          _..----.._       |\/\||//||||
        .'     o    '.     |||\\|/\\ ||
       /   o       o  \    | './\_/.' |
      |o        o     o|   |          |
      /'-.._o     __.-'\   |          |
      \      `````     /   |          |
      |``--........--'`|    '.______.'
       \              /
        `'----------'`    
""")
    s_print(f"{colours.fg.blue}A Burger King? What the- How?")
    s_print("You enter...")
    s_print(f"{colours.fg.red}Welcome traveller! What would you like today?")

    # Loop until we're leaving
    while True:
        # Ask for user input
        menu = Menu("Select one", None, [
            "What is this place?",
            "Yeah, can I have a burger please?",
            "I'm.. going to go..."
        ])
        response, _ = menu.Start()
        s_print(f"{colours.fg.blue}{response}")
        
        # Breaking out
        if (response == "I'm.. going to go..."):
            s_print(f"{colours.fg.red}Goodbye! Have a great day!")
            break

        # Asking what this place it
        if (response == "What is this place?"):
            
            s_print(f"{colours.fg.red}Burger King. Have you not read the sign?")
            s_print(f"{colours.fg.blue}But how are you still alive? We are literally in a post-apocalypse world.")
            s_print(f"{colours.fg.red}Well anything is possible, with the power of Christ!")
            s_print(f"{colours.fg.blue}Okay... ?")
            continue

        # Ordering burger
        if (response == "A burger (2 Ammo) please."):
            s_print(f"{colours.fg.red}That will be 2 Ammo sir.")

            # Check if we have enough ammo
            if (game.ammo < 2):
                s_print("You look hastily through your bag...")
                s_print(f"{colours.fg.blue}I'm sorry, I can't afford it...")
                s_print(f"{colours.fg.red}Oh. Well..")
                s_print("The silence got louder, and the air stale...")
                s_print(f"{colours.fg.blue}Nevermind.")
                continue

            # Dialog and taking ammo
            s_print("You hand the ammo across...")
            game.ammo -= 2
            print(f"{colours.fg.red}-2 Ammo{colours.reset}")
            s_print(f"{colours.fg.red}Coming right up! Please wait...")
            s_print(f"{colours.fg.blue}Hold on. What order number am I?")
            s_print(f"{colours.fg.red}Order 69.")
            s_print("The sound of fizzling oil can be heard from the kitchen behind, and before you know it, ding!")
            s_print(f"{colours.fg.red}Order up! Order 69?")
            s_print("You take your burger, sit down, and eat it..")
            s_print(f"{colours.fg.blue}Mmm, delicious.")
            print(f"{colours.fg.green}+1 Health{colours.reset}")
            game.hp += 1

    # Leaving
    s_print("You leave the shop, perplexed, wondering how it's still operational but thankful that some civilisation still exists.")
@event
def Food_Survivor(game: Game):
    # Intro
    s_print("You find a desolate person on the road... They seem hungry.")
    s_print("They seem unresponsive...")

    # Get user response
    menu = Menu("Will you offer them one food?", None, [
        "Yes",
        "No"
    ])
    response, _ = menu.Start()

    # No
    if (response == "No"):
        s_print("You just walk past...")
        return False

    # Yes
    s_print("You hand them food...")
    print(f"{colours.fg.red}-1 Food")
    s_print("They said nothing... You walk away, as you got further away, they started to follow you.")
    medicChance = randint(1, 10) <= 5
    survivor = Medic() if medicChance else Survivor()
    s_print(f"{colours.fg.green}+1 {survivor.type}")
    game.survivors.append(survivor)

# Survivor events
@event
def Survivor_Survivor(game: Game):
    # Intro
    print("""
      /:""|       .@@@@@,
     |: 66|_      @@@@@@@@,
     C     _)     aa`@@@@@@
      \ ._|      (_   ?@@@@
       ) /        =' @@@@"
      /`\\         \(```
     || |Y|       //`\        ."~~~~~".
     || |#|      / | ||       |  .:.  |
     || |#|      \ | ||    A  | /6 6\ |
     || |#|      / | ||   |~|_|_\ e /_|_     .@@@@,
     :| |=:     /  | |\   |_|)___`"`___(8    aa`@@@,
     ||_|,|    |   |_| \     |~~~~~~~~~|     =  `@@@
     \)))||    |   (((  |    \_________/       )_/`@'
  |~~~`-`~~~|  `~\~~~~~~|     |/ /_\ \|       / || @
  |         |     `\   /      ()/___\()       | || @
  |_________|       ( ||      ||~~~~~||       /~|| "`
  |_________|       | ||      ||     ||      /__W_\
      | ||          | ||      ||     ||        |||
      |_||__      __|_||      ||_____||       _|||
      (____))    (:;:;))      ||-----||      ((___)
""")
    s_print("You find a pact of survivors working together...")
    s_print("They approach you...")
    s_print(f"{colours.fg.red}Hello, how are you?")

    # Ask the user for input
    menu = Menu("Select one", None, [
        "I'm alright, you?",
        "Who are you guys?"
    ])
    response, _ = menu.Start()

    #
    s_print(f"{colours.fg.blue}{response}")
    if (response == "I'm alright, you?"):
        s_print(f"{colours.fg.red}Great, thanks for asking!")
    else:
        s_print(f"{colours.fg.red}Getting straight to the point, aren't we?")

    #
    s_print(f"{colours.fg.red}We are the 6 Flag Commitee and we, help... others survivors. But of course, everything has a price.")
    s_print(f"{colours.fg.blue}A price...? What price? What reward even?")
    s_print(f"{colours.fg.red}Well, we get bored around here a lot so we would like some entertainment... Guys, what do we all like?")
    s_print("They all say collectively,")
    s_print(f"{colours.fg.red}BLOOD!")
    s_print(f"{colours.fg.red}So what do you say, are you in or out?")
    s_print(f"{colours.fg.blue}Wait, you haven't said what I get out of it..")
    s_print(f"{colours.fg.red}Glory, wealth, and success!")

    # Ask for user input
    menu2 = Menu("What will you do?", None, [
        "Participate",
        "Run away"
    ])
    response2, _ = menu2.Start()

    # Running away
    if (response == "Run away"):
        s_print(f"{colours.fg.red}Running away, are we?")
        s_print(f"{colours.fg.red}Oh well, your loss...")
        return False

    # Participate
    s_print(f"{colours.fg.red}Good choice. Let the fun begin!")
    s_print(f"{colours.fg.blue}So, what am I doing..?")
    zombieCount = randint(3, 10)
    s_print("You black out and wake up in a hole..")
    s_print(f"Before you know it, there are {zombieCount} zombies approaching you.")

    # Quick time events
    for i in range(zombieCount):
        s_print("A zombie runs for your head", 0.01, 0.025)
        randomLetter = choice(string.ascii_letters).upper()
        givenInput = time_input(f"Press {randomLetter}") # randomise this

        # Check if we died
        if (game.hp <= 0):
            return True

        # Did not input
        if (not givenInput or givenInput != randomLetter):
            s_print("Incorrect. You failed the attack but still managed to kill the zombie at the cost of one health")
            print(f"{colours.fg.red}-1 Health{colours.reset}")
            game.hp -= 1

        # Zombie died
        s_print(f"{colours.fg.blue}Bring on the next one!", 0.05, 0.025)

    #
    s_print(f"{colours.fg.blue}That was one entertaining fight. Well done!")
    print(f"{colours.fg.green}+10 Food{colours.reset}")
    s_print("You walk away, it was a tough battle. Was it worth it?")