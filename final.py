# JF & DS Keyboard Dungeon

import keyboard
import time
import os



class Player:
    def __init__(self):
        self.room = 0
        self.coord = (3,3) #MAKE THIS CORRECT LATER
        self.inventory = ["Shortsword"]

    #def 

class Enemy:
    def __init__(self, kind, room, coord):
        self.kind = kind
        self.room = room
        self.coord = coord
    
    def behavior():
        pass

def display():
    pass

def main():
    while True:
        char = input("Select a letter to play as: ").capitalize()
        if len(char) > 1:
            print("You can't play as more than one letter. Try again.")
            continue
        if not char.isalpha():
            print("That's not an alphabetic letter. Try again.")
            continue
        else:
            break


    _ = input(f"""You are {char}.
LORELORELORE

Use the arrow keys (or WASD) to move
Use E to open the inventory
Use LMB to attack with your chosen weapon
Use SPACE to open chests(☐) or doors (|,-)(You have to be next to them to open them)

Press ENTER to start your adventure!
""")

        
    while True:

        if keyboard.is_pressed("esc"): break
        time.sleep(0.1)

main()

def invent():
    if keyboard.is_pressed("E"):
        pass
