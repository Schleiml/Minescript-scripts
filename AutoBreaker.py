import minescript as m
from minescript import press_key_bind
import time
from time import sleep
import re
from minescript_plus import Inventory

m.execute("/effect give @a minecraft:haste infinite 250")
m.execute("/give @a minecraft:wooden_pickaxe")

stop_flag = False # is a on/off thing for the main Loop at the end

# The dictionary for all the types of materials and their HP
durability = {
    "wooden": 59,
    "stone": 131,
    "iron": 250,
    "golden": 32,
    "diamond": 1561,
    "netherite": 2031
}

PickenSlot = 0

# it's a function for swaping the pickaxe when it's about to break

def Swap_Pickaxe():
    global PickenSlot
    global stop_flag
    tool = "pickaxe" # it's for checking if you have a pickaxe in ur inventory
    inv = m.player_inventory() # checks the whole inventory
    found = False # just a variable when it found a available pickaxe

    for item in inv: # checks every single item 
        if tool in item.item: # if theres an pickaxe 
            max_dur = 1000 # this is just puffer when theres no number or material or something
            for material in durability: # it's go through every material
                    if material in item.item: # it's checks if the material is in the name of the tool
                        max_dur = durability[material] # makes the durability of their material
                        break
            match = re.search(r'"minecraft:damage":(\d+)', item.nbt or "") # checks how often the tool was used, from the nbt-data
            damage = int(match.group(1)) if match else 0 # and makes that to an number

            if max_dur - damage >= 10: # checks if the tool has more than 10 HP 
                PickenSlot = item.slot # gives the slot to the variable
                found = True
                break

    if not found: # it's just there for when theres no tool detected so its stopps the breaking and u can no longer hold the attack button
        stop_flag = True
        print("no pick!!!!")
        press_key_bind("key.attack", False)
        return

    m.player_inventory_select_slot(PickenSlot) # switches to the slot where the tool is

def check_durability():
    global stop_flag
    tool = m.player_hand_items().main_hand # checks if theres something in the main-hand
    if not tool: # if theres nothing in the hand it's stopps the programm
        return
    tool_name = tool.item # saves the name
    tool_damage = tool.nbt or "" # saves the nbt-data
    match = re.search(r'"minecraft:damage":(\d+)', tool_damage) 
    damage = int(match.group(1)) if match else 0

    tool_durability = 1000 # this is just puffer when theres no number or material or something
    for material in durability: 
        if material in tool_name:
            tool_durability = durability[material]

    if tool_durability - damage <= 10: # checks if the tool was used less or even than 10 times
        Swap_Pickaxe()
    sleep(0.1)

while True:
    check_durability()
    if stop_flag:
        m.echo("Script stopps!!!")
        break
