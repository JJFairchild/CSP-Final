# JF & DS Keyboard Dungeon

import keyboard
import random
import time
import os

class Player:
    def __init__(self):
        self.health = 100
        self.room = 0
        self.coord = (3,3) #MAKE THIS CORRECT LATER
        self.inv = ["Sword"]
        self.weapon = "Sword"
        
    def interact(self):
        #Look for surrounding chests/doors
        #if a chest is found call choose_item() on it and add the result to the inventory
        pass

num_potion = 0

    def use(self):
            pass
        if keyboard.is_pressed("e"):
            def we():
                os.system("cls")
                if keyboard.is_pressed("x"):
                    #need val to cont game
                else:
                    print("Select an item to use:")
                    for item in self.inv:
                    print(f"- {item}")
            
                    item = input()
                    if item in self.inv:
                        if item == "Potion":
                            if num_potoin <= 0:
                                print("You don't have any Potions")
                                we()
                            else: 
                                self.health += 50
                                num_potion -= 1
                                if self.health > 100: self.health == 100
                                we()
                        elif item == "Sword":
                            self.weapon = "Sword"
                            we()
                        elif item == "Spear":
                            self.weapon = "Spear"
                            we()
                        elif item == "Bomb":
                            self.weapon = "Bomb"
                            we()
                        else:
                            print("Not in inventory")
                            we()
                    else:
                        print("Not in inventory")
                        we()
                       

class Enemy:
    def __init__(self, kind, coord):
        self.kind = kind
        self.coord = coord
    
    def behavior():
        pass

class Wall:
    def __init__(self, coord):
        self.coord = coord

class Door:
    def __init__(self, coord, orientation, new_room):
        self.coord = coord
        self.orientation = orientation
        self.new_room = new_room

class Chest:
    def __init__(self, contents, coord):
        self.contents = contents
        self.coord = coord
        self.table = [("Bomb", 0.1), ("Spear", 0.1), ("Potion", 0.4)]
        
       
    def choose_item(self):
        while True:
            item = random.choice(self.table)
            if random.random() < item[1]:
                return item[0]
    if item = "Potion":
        num_potion += 1

game = [
    {},
    {},
    {},
    {},
    {},
    {},
    {},
    {},
    {},
    {},
    {},
    {}
]

def area(x1, y1, x2, y2):
    tiles = []
    for i in range(x1, x2+1):
        for j in range(y2, y1, -1):
            tiles.append((i,j))
    return tiles

def display():
    os.system("cls")
    

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
