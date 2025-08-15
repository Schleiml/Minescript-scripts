import minescript as m
from minescript import press_key_bind
import time
from time import sleep
import re
from minescript_plus import Inventory

m.execute("/effect give @a minecraft:haste infinite 250")
m.execute("/give @a minecraft:wooden_pickaxe")

stop_flag = False

durability = {
    "wooden": 59,
    "stone": 131,
    "iron": 250,
    "golden": 32,
    "diamond": 1561,
    "netherite": 2031
}

PickenSlot = 0

def Swap_Pickaxe():
    global PickenSlot
    global stop_flag
    tool = "pickaxe"
    inv = m.player_inventory()
    found = False

    for item in inv:
        if tool in item.item:
            max_dur = 1000
            for material in durability:
                    if material in item.item:
                        max_dur = durability[material]
                        break
            match = re.search(r'"minecraft:damage":(\d+)', item.nbt or "")
            damage = int(match.group(1)) if match else 0

            if max_dur - damage >= 10:
                PickenSlot = item.slot
                found = True
                break

    if not found:
        stop_flag = True
        print("no pick!!!!")
        press_key_bind("key.attack", False)
        return

    m.player_inventory_select_slot(PickenSlot)

def check_durability():
    global stop_flag
    tool = m.player_hand_items().main_hand
    if not tool:
        return
    tool_name = tool.item
    tool_damage = tool.nbt or ""
    match = re.search(r'"minecraft:damage":(\d+)', tool_damage)
    damage = int(match.group(1)) if match else 0

    tool_durability = 1000
    for material in durability:
        if material in tool_name:
            tool_durability = durability[material]

    if tool_durability - damage <= 10:
        Swap_Pickaxe()
    sleep(0.1)

while True:
    check_durability()
    if stop_flag:
        m.echo("Script stopps!!!")
        break
