import minescript as m
from minescript_plus import Inventory, Gui
import time

gold = "apple"
sword = "sword"
run = True


m.echo("starts script")

def search_apple():
    for item in m.player_inventory():
        name = item.item
        if gold in name:
            return item.slot

def search_sword():
    for item in m.player_inventory():
        name = item.item
        if sword in name:
            return item.slot

while run:
    health = m.player_health()
    heal_slot = search_apple()
    sword_slot = search_sword()

    if health <= 8 and heal_slot is not None:
        m.player_inventory_select_slot(heal_slot)
        m.player_press_use(True)
    elif health >= 9 and sword_slot is not None:
        m.player_press_use(False)
        m.player_inventory_select_slot(sword_slot)