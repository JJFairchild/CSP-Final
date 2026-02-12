# JF & DS Keyboard Dungeon

import keyboard
import random
import time
import os

# Classes for all displayable tiles (including player and enemies) --------------------------------------------------------

class Player:
    def __init__(self, char):
        self.health = 100
        self.room = 0
        self.char = char
        self.coord = (5,7)
        self.inv = ["Sword"]
        self.weapon = "Sword"
        
    def interact(self, map):
        for tile in map.values():
            if type(tile) == Chest and tile.coord in area((),()):
                pass

        #if a chest is found call choose_item() on it and add the result to the inventory

    def inventory(self):
        os.system("cls")
        
        while True:
            print("Select an item to use (or type 'Exit' to cancel): ")
            for item in self.inv:
                print(f"- {item}")
            
            item = input().strip().capitalize()
            if item in self.inv:
                if item == "Health Potion":
                    self.health += 50
                    if self.health > 100: self.health == 100
                    self.inv.remove("Health Potion")
                elif item == "Sword": self.weapon = "Sword"
                elif item == "Spear": self.weapon = "Spear"
                elif item == "Bomb": self.weapon = "Bomb"
                
            elif item == "Exit": break
            print()

    def useWeapon(self):
        pass

class Enemy:
    def __init__(self, kind, coord):
        self.char = kind
        if kind == "*":
            self.health = 25 # fix these values later
            self.dmg = 10
        elif kind == "0":
            self.health = 100
            self.dmg = 20
        else:
            self.health = 500
            self.dmg = 50
        self.coord = coord

        self.lastAtt = time.time()
    
    def behavior(self, player):
        if self.char == "0" and time.time() - self.lastAtt < 0.2: return
        if self.char == "%" and time.time() - self.lastAtt < 0.3: return

        if player.coord in area((self.coord[0]-1, self.coord[1]-1),(self.coord[0]+1, self.coord[1]+1)):
            return player.health - self.dmg
        else:
            pass

        

class Wall:
    def __init__(self, coord):
        self.char = "█"
        self.coord = coord

class Door:
    def __init__(self, coord, orientation, new_room, new_coord):
        self.coord = coord
        self.char = orientation
        self.new_room = new_room
        self.new_coord = new_coord

class Chest:
    def __init__(self, coord):
        self.char = "☐"
        self.coord = coord
        self.table = [("Bomb", 0.05), ("Spear", 0.1), ("Health Potion", 0.4)]
        
    def chooseItem(self):
        while True:
            item = random.choice(self.table)
            if random.random() < item[1]:
                return item[0]
            
class Trap:
    def __init__(self, coord):
        self.char = "#"

    def activate(self):
        pass

# Helper functions / variables --------------------------------------------------------

game = [
    {(x, y): Wall((x, y)) for x, y in zip(
        [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 2, 17, 1, 18, 1, 1, 1, 18, 1, 18, 1, 18, 1, 1, 1, 18, 2, 17, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 3, 3, 4, 5, 6, 6, 7, 7, 8, 8, 9, 10, 11, 11, 12, 12, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13]
    )} | {(18, 4): Door((18, 4), "|", 1, (2,7)), (18, 5): Door((18, 5), "|", 1, (2,8)), (18, 9): Door((18, 9), "|", 2, (2,2)), (18, 10): Door((18, 10), "|", 2, (2,3))},
    
    {(x, y): Wall((x, y)) for x, y in zip(
        [12, 13, 14, 15, 16, 17, 18, 19, 12, 19, 12, 19, 12, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 19, 19, 19, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
        [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 3, 3, 4, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 7, 8, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
        )} | {},
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

def area(coord1, coord2):
    tiles = []
    x1, y1 = coord1
    x2, y2 = coord2
    x_start, x_end = min(x1, x2), max(x1, x2)
    y_start, y_end = min(y1, y2), max(y1, y2)
    for y in range(y_start, y_end + 1):
        for x in range(x_start, x_end + 1):
            tiles.append((x, y))
    return tiles

def move(player):
    dx = 0
    dy = 0

    if keyboard.is_pressed("up") or keyboard.is_pressed("w"): dy = -1
    if keyboard.is_pressed("down") or keyboard.is_pressed("s"): dy = 1
    if keyboard.is_pressed("left") or keyboard.is_pressed("a"): dx = -1
    if keyboard.is_pressed("right") or keyboard.is_pressed("d"): dx = 1

    new_coord = (player.coord[0] + dx, player.coord[1] + dy)
    room = game[player.room]
    tile = room.get(new_coord)

    if isinstance(tile, Door):
        player.room = tile.new_room
        player.coord = tile.new_coord
        return

    for coord in area(player.coord, new_coord): 
        if coord in room: return

    player.coord = new_coord

def pathfind(player, enemy):
    

def display(player):
    os.system("cls")

    prevY = 1
    for coord in area((0,0), (max([k[0] for k in game[player.room].keys()])+1, max([k[1] for k in game[player.room].keys()])+1)):
        if prevY != coord[1]: print()
        try: print(game[player.room][coord].char, end="")
        except: 
            if coord == player.coord: print(player.char, end="")
            else: print(" ", end="")
        prevY=coord[1]

# Main loop --------------------------------------------------------

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
Use SPACE to open chests(☐)

Press ENTER to start your adventure!
""")

    player = Player(char)
        
    while True:
        if keyboard.is_pressed("e"): player.inventory()
        if keyboard.is_pressed("esc"): break

        if player.health == 0:
            print("")
            break
        move(player)
        display(player)
        time.sleep(.075)

main()