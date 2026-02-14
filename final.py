# JF & DS Keyboard Dungeon
# "import" adds things from an external library to the code. JF coded this.

import keyboard
import random
import time
import os

# Classes for all displayable tiles (including player and enemies) ------------------------------------------------------------------
# The classes are defining our player and other elements like walls, doors, etc. 
# Classes coded by JF. Inventory coded by DS and polished by JF.

class Player:
    def __init__(self, char):
        self.health = 100
        self.max_health = 100
        self.room = 0
        self.char = char
        self.coord = (5,7)
        self.inv = ["Sword", "Bomb"]
        self.weapon = "Sword"
        self.lastAtt = time.time()
        
    def openChest(self, game):
        os.system("cls")

        for chest in game[self.room]["chests"]:
            if chest.coord in getNeighbors(self.coord):
                while True:
                    item = chest.chooseItem()
                    if item in ["Bomb"] and item in self.inv: continue
                    break
                input(f"You got a {item}!\nPress ENTER to continue.\n")
                self.inv.append(item)

                del game_coords[self.room][chest.coord]
                game[self.room]["chests"].remove(chest)

    def inventory(self):
        os.system("cls")
        
        while True:
            print(f"Health: {self.health}\nSelect an item to use (or type 'Exit' to cancel): ")
            for item in self.inv:
                print(f"- {item}")
            
            item = input().strip().title()
            if item in self.inv:
                if item == "Health Potion":
                    self.health += 50
                    if self.health > self.max_health: self.health = self.max_health
                    self.inv.remove("Health Potion")
                    print("Used health potion!")
                elif item == "Armor":
                    self.max_health *= 1.5
                    self.inv.remove("Armor")
                elif item == "Sword":
                    self.weapon = "Sword"
                    print("Equipped sword! This weapon will damage all enemies that are near you.")
                elif item == "Bomb":
                    self.weapon = "Bomb"
                    print("Equipped bomb! This weapon will significantly damage all enemies in a large area to the right but are one-use.")
                
            elif item == "Exit": break
            else: print("You don't have that item. Try again.")
            print()

    def useWeapon(self):
        if self.weapon == "Sword" and time.time() - self.lastAtt >= 0.2:
            for enemy in game[self.room]["enemies"]:
                if enemy.coord in getNeighbors(self.coord): enemy.health -= 50
            self.lastAtt = time.time()
        if self.weapon == "Bomb" and time.time() - self.lastAtt >= 1:
            for enemy in game[self.room]["enemies"]:
                if enemy.coord in area((self.coord[0]+2, self.coord[1]+2), (self.coord[0]+6, self.coord[1]-2)): enemy.health -= 100
            self.inv.remove("Bomb")
            self.weapon = None
            bomb_animation((self.coord[0], self.coord[1]+4))
            self.lastAtt = time.time()
            

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
        if self.char == "*" and time.time() - self.lastAtt < 0.2: return player.health
        if self.char == "0" and time.time() - self.lastAtt < 0.4: return player.health
        if self.char == "%" and time.time() - self.lastAtt < 0.6: return player.health
        self.lastAtt = time.time()

        if player.coord in getNeighbors(self.coord) or (self.char == "%" and player.coord in list(set([item for sublist in [getNeighbors(neighbor) for neighbor in getNeighbors(self.coord)] for item in sublist]))):
            return player.health - self.dmg
        else:
            coord = pathfind(player, self)
            self.coord = coord
            return player.health

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
        self.table = [("Bomb", 0.1), ("Armor", .25), ("Health Potion", 0.5)]
        
    def chooseItem(self):
        while True:
            item = random.choice(self.table)
            if random.random() < item[1]:
                return item[0]
            
class Trap:
    def __init__(self, coord):
        self.char = "#"
        self.coord = coord

# Helper functions / variables --------------------------------------------------------
# This definition makes it so the rooms appear on the terminal and places walls, doors, chests, enemies, and traps in specific locations.
# Coded by JF

def makeDisplayable(room):
    new_room = {}
    for category in game[room].values():
        for tile in category:
            new_room.update({tile.coord: tile})

    return new_room

game = [
    {
        "walls": [Wall(coord) for coord in [(3,1),(4,1),(5,1),(6,1),(7,1),(8,1),(9,1),(10,1),(11,1),(12,1),(13,1),(14,1),(15,1),(16,1),(2,2),(17,2),(1,3),(18,3),(1,4),(1,5),(1,6),(18,6),(1,7),(18,7),(1,8),(18,8),(1,9),(1,10),(1,11),(18,11),(2,12),(17,12),(3,13),(4,13),(5,13),(6,13),(7,13),(8,13),(9,13),(10,13),(11,13),(12,13),(13,13),(14,13),(15,13),(16,13)]],
        "doors": [Door((18, 4), "|", 1, (2,7)), Door((18, 5), "|", 1, (2,8)), Door((18, 9), "|", 2, (2,2)), Door((18, 10), "|", 2, (2,3))],
        "chests": [],
        "enemies": [],
        "traps": []
    },
    {
        "walls": [Wall(coord) for coord in [(12,1),(13,1),(14,1),(15,1),(16,1),(17,1),(18,1),(19,1),(12,2),(19,2),(12,3),(19,3),(12,4),(12,5),(1,6),(2,6),(3,6),(4,6),(5,6),(6,6),(7,6),(8,6),(9,6),(10,6),(11,6),(12,6),(19,6),(19,7),(19,8),(1,9),(2,9),(3,9),(4,9),(5,9),(6,9),(7,9),(8,9),(9,9),(10,9),(11,9),(12,9),(13,9),(14,9),(15,9),(16,9),(17,9),(18,9),(19,9)]],
        "doors": [Door((1, 7), "|", 0, (17,3)), Door((1, 8), "|", 0, (17,4)), Door((19, 4), "|", 2, (2,2)), Door((19, 5), "|", 2, (2,3))],
        "chests": [Chest((13, 2))],
        "enemies": [Enemy("0", (15,3)), Enemy("0", (16,6))],
        "traps": [Trap((9,8))]
    },
    {
        "walls": [Wall(coord) for coord in [(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(8,1),(9,1),(10,2),(10,3),(1,4),(2,4),(3,4),(4,4),(5,4),(6,4),(10,4),(7,5),(10,5),(7,6),(10,6),(7,7),(10,7),(7,8),(10,8),(7,9),(10,9),(11,9),(12,9),(7,10),(7,11),(8,12),(9,12),(10,12),(11,12),(12,12)]],
        "doors": [Door((1, 2), "|", 1, (16,4)), Door((1, 3), "|", 1, (16,5)), Door((12, 10), "|", 3, (2,5)), Door((12, 11), "|", 3, (2,6))],
        "chests": [Chest((7,4))],
        "enemies": [Enemy("*", (10,10))],
        "traps": [Trap((9,2)), Trap((8,9))]
    },
    {
        "walls": [Wall(coord) for coord in [(2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(8,1),(9,1),(10,1),(11,1),(2,2),(11,2),(2,3),(11,3),(1,4),(2,4),(11,4),(11,5),(11,6),(1,7),(2,7),(11,7),(2,8),(3,8),(4,8),(5,8),(6,8),(9,8),(10,8),(11,8),(6,9),(9,9),(6,10),(9,10)]],
        "doors": [Door((1,5), "|", 2, (11,10)), Door((1,6), "|", 2, (11,11)), Door((7,10), '-', 4, (8, 2)), Door((8,10), '-', 4, (9, 2))],
        "chests": [Chest((10,5)), Chest((4,7))],
        "enemies": [Enemy('0', (5,4))],
        "traps": []
    },
    {
        "walls": [Wall(coord) for coord in [(7,1), (10,1), (7,2), (10,2), (5,3), (6,3), (7,3), (10,3), (5,4), (11,4), (5,5), (12,5), (5,6), (13,6), (5,7), (13,7), (5,8), (13,8), (4,9), (13,9), (14,9), (15,9), (16,9), (4,10), (4,11), (4,12), (13,12), (14,12), (15,12), (16,12), (4,13), (13,13), (4,14), (13,14), (4,15), (13,15), (4,16), (13,16), (3,17), (12,17), (1,18), (2,18), (3,18), (12,18), (11,19), (8,20), (9,20), (10,20), (1,21), (2,21), (3,21), (4,21), (5,21), (6,21), (7,21)]],
        "doors": [Door((8,1), '-', 3, (7, 9)), Door((9,1), '-', 3, (8, 9)), Door((16,10), '|', 11, (2, 7)), Door((16,11), '|', 11, (2, 8)), Door((1,19), '|', 5, (18, 6)), Door((1,20), '|', 5, (18, 7))],
        "chests": [Chest((5,9))],
        "enemies": [Enemy('0', (10,12)), Enemy('*', (9,14))],
        "traps": [Trap((12,8))]
    },
    {
        "walls": [],
        "doors": [],
        "chests": [],
        "enemies": [],
        "traps": []
    },
    {
        "walls": [],
        "doors": [],
        "chests": [],
        "enemies": [],
        "traps": []
    },
    {
        "walls": [],
        "doors": [],
        "chests": [],
        "enemies": [],
        "traps": []
    },
    {
        "walls": [],
        "doors": [],
        "chests": [],
        "enemies": [],
        "traps": []
    },
    {
        "walls": [],
        "doors": [],
        "chests": [],
        "enemies": [],
        "traps": []
    },
    {
        "walls": [],
        "doors": [],
        "chests": [],
        "enemies": [],
        "traps": []
    },
    {
        "walls": [Wall(coord) for coord in [(1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (7,1), (8,1), (9,1), (10,1), (11,1), (12,1), (13,1), (14,1), (15,1), (16,1), (17,1), (18,1), (19,1), (20,1), (21,1), (22,1), (23,1), (24,1), (25,1), (26,1), (27,1), (28,1), (29,1), (30,1), (31,1), (1,2), (32,2), (33,2), (1,3), (34,3), (1,4), (34,4), (1,5), (35,5), (1,6), (35,6), (1,7), (35,7), (1,8), (35,8), (1,9), (35,9), (1,10), (35,10), (1,11), (35,11), (1,12), (34,12), (1,13), (34,13), (1,14), (32,14), (33,14), (1,15), (2,15), (3,15), (4,15), (5,15), (6,15), (7,15), (8,15), (9,15), (10,15), (11,15), (12,15), (13,15), (14,15), (15,15), (16,15), (17,15), (18,15), (19,15), (20,15), (21,15), (22,15), (23,15), (24,15), (25,15), (26,15), (27,15), (28,15), (29,15), (30,15), (31,15)]],
        "doors": [],
        "chests": [],
        "enemies": [Enemy('0', (12,4)), Enemy('0', (12,8)), Enemy('%', (28,8)), Enemy('0', (12,12))],
        "traps": [Trap((17,3)), Trap((8,5)), Trap((23,6)), Trap((19,8)), Trap((5,12)), Trap((28,12))]
    },
]

game_coords = [
    makeDisplayable(0),
    makeDisplayable(1),
    makeDisplayable(2),
    makeDisplayable(3),
    makeDisplayable(4),
    makeDisplayable(5),
    makeDisplayable(6),
    makeDisplayable(7),
    makeDisplayable(8),
    makeDisplayable(9),
    makeDisplayable(10),
    makeDisplayable(11),
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
# This bomb animation adds a visual effect so the player can see where the bomb goes off. Coded by JF.
def bomb_animation(center):
    frames = [
        ["   ",
         " * ",
         "   "],
        [" * ",
         "***",
         " * "],
        ["***",
         "***",
         "***"],
        [" * ",
         "***",
         " * "],
        ["   ",
         " * ",
         "   "]
    ]
# This loop clears the screen. Coded by JF
    for frame in frames:
        os.system("cls")

        for _ in range(center[1]-5): print()
        for i in range(len(frame)):
            for _ in range(center[0]+1): print(" ", end="")
            print(frame[i],end="")
            print()
        time.sleep(.2)

def getNeighbors(coord):
    return area((coord[0]-1, coord[1]-1),(coord[0]+1, coord[1]+1))

def getMax(room):
    mapping = game_coords[room]
    if not mapping: return (1, 1)
    return (max([coord[0] for coord in mapping.keys()]) + 1, max([coord[1] for coord in mapping.keys()]) + 1)
# This allows the player to move using the keyboard. Coded by JF.
def move(player):
    dx = 0
    dy = 0

    if keyboard.is_pressed("up") or keyboard.is_pressed("w"): dy -= 1
    if keyboard.is_pressed("down") or keyboard.is_pressed("s"): dy += 1
    if keyboard.is_pressed("left") or keyboard.is_pressed("a"): dx -= 1
    if keyboard.is_pressed("right") or keyboard.is_pressed("d"): dx += 1

    new_coord = (player.coord[0] + dx, player.coord[1] + dy)
    tile = game_coords[player.room].get(new_coord)
# This allows the player to enter new rooms through doors. Coded by JF.
    if isinstance(tile, Door):
        player.room = tile.new_room
        player.coord = tile.new_coord
        return

    if isinstance(tile, (Wall, Chest)): return

    player.coord = new_coord

def hasClearLOS(start, end, room_num): # Uses Bresenham's algorithm to find tiles on the line of sight! (I'm so happy I figured this out lol) Coded by JF.
    x1, y1 = start
    x2, y2 = end
    
    # Line steepness. Coded by JF.
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    # Direction (up/down and left/right). Coded by JF.
    sx = 1 if x2 > x1 else -1
    sy = 1 if y2 > y1 else -1

    err = dx - dy # How far off the ideal line a point is. Coded by JF.
    
    room_map = game_coords[room_num]
    
    while (x1, y1) != (x2, y2):
        if (x1, y1) != start and isinstance(room_map.get((x1, y1)), Wall):
            return False
        
        e2 = err * 2
        
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy
    
    return True

# Allows the enemy to find the player. Coded by JF.
def pathfind(player, enemy):
    if not hasClearLOS(enemy.coord, player.coord, player.room): return enemy.coord

    dx = 0
    dy = 0
    if player.coord[0] > enemy.coord[0]: dx += 1
    if player.coord[0] < enemy.coord[0]: dx -= 1
    if player.coord[1] > enemy.coord[1]: dy += 1
    if player.coord[1] < enemy.coord[1]: dy -= 1
    
    new_coord = (enemy.coord[0] + dx, enemy.coord[1] + dy)
    if isinstance(game_coords[player.room].get(new_coord), (Wall, Chest, Enemy)): return enemy.coord
    return new_coord

def display(player):
    os.system("cls")

    if player.room == 11:
        for enemy in game[player.room]["enemies"]:
            if enemy.char == "%": boss = enemy

    prevY = None
    for coord in area((0, 0), getMax(player.room)):
        if prevY is None: prevY = coord[1]
        if prevY != coord[1]: print()
        tile = game_coords[player.room].get(coord)
        if tile: print(tile.char, end="")
        elif player.room == 11 and coord in getNeighbors(boss.coord): print("%", end="")
        elif coord == player.coord: print(player.char, end="")
        else: print(" ", end="")
        prevY = coord[1]
    print(f"\nHealth: {player.health}")

# Main --------------------------------------------------------
# Tutorial intro uses inputs and conditionals to allow the player to select a letter from the alphabet as their identity/name. Coded by DS with input from JF.
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
# Lore and player instructions/controls written by DS.
    _ = input(f"""You are {char}.
Welcome, chosen hero of the prophecy! It has been foretold that you shall enter the Dungeon of Keys.
Slay the beast of Percentistan (%) and fight of his minions the Ratsterisks (*) and Gobnones (0)!
These monsters have set up traps (#). If you step on them they will hurt you!
It is said the hero will enter with their sword but may need a Spear to attack lined up monsters
and a Bomb to fight from afar. But beware! You'll have to find these weapons in the many chests of
the Dungeon of Keys. 
              
Use E to open your inventory
To use something from your inventory, type it in. Capitalize the first letter! This is how you
swap weapons and consume potions.
Use a Potion from your inventory to restore your health. 

Use the arrow keys (or WASD) to move
Use SPACE to attack with your chosen weapon
Use X to open chests(☐) that are next to you
Anything you find in a chest will automatically be added to your inventory.

Press ENTER to start your adventure!
""")

    player = Player(char)
        
    while True:
        if keyboard.is_pressed("x"): player.openChest(game)
        if keyboard.is_pressed("space"): player.useWeapon()
        if keyboard.is_pressed("e"): player.inventory()
        if keyboard.is_pressed("esc"): break

        for trap in game[player.room]["traps"]:
            if trap.coord == player.coord:
                del game_coords[player.room][trap.coord]
                game[player.room]["traps"].remove(trap)
                player.health -= 50

        move(player)

        for enemy in game[player.room]["enemies"]:
            if enemy.health <= 0:
                del game_coords[player.room][enemy.coord]
                game[player.room]["enemies"].remove(enemy)
            player.health = enemy.behavior(player)
# Ends the game and tells the player they've died when they reach negative health points. Coded by JF. Message by DS.
        if player.health <= 0:
            print("You have died.")
            break
# Ends the game and tells the player they've won when they are in final boss room and boss is dead. Coded by JF. Message by DS.
        if player.room == 11 and "%" not in [enemy.char for enemy in game[player.room]["enemies"]]:
            print("You slayed beast of Percentistan! You will be remembered as the greatest hero of all time!")
            break

        if player.health < player.max_health: player.health = round(player.health + .1, 1)

        game_coords[player.room] = makeDisplayable(player.room)
        display(player)
        time.sleep(.1)

main()