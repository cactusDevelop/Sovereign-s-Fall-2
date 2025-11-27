
import json

from characters import Player
from weapon import Weapon
from object import Object
from constants import _CST_DATA, _HS


def get_cst_names():
    return _CST_DATA["monster_names"], _CST_DATA["boss_names"], _CST_DATA["weapon_names"]

def save_hs(nickname, score, level):
    _HS["history"].append({"nickname": nickname, "score": int(score), "level": int(level)})
    _HS["history"] = sorted(_HS["history"], key=lambda x: x["score"], reverse=True)[:10]
    if score > _HS["highscore"]:
        _HS["highscore"] = score
    with open("JSON/highscores.json", "w", encoding="utf-8") as write_file:
        json.dump(_HS, write_file, ensure_ascii=False, indent=4)
    return _HS["highscore"]


# SAVED VARIABLES
with open("JSON/active_data.json", "r", encoding="utf-8") as read_file:
    data = json.load(read_file)

def save_game(new_player, level=1, used_monsters=None, max_inv_size=None):
    data["player"]["nickname"] = new_player.name
    data["player"]["pv"] = new_player.pv
    data["player"]["max_pv"] = new_player.max_pv
    data["player"]["stim"] = new_player.stim
    data["player"]["max_stim"] = new_player.max_stim
    data["player"]["current_level"] = level

    if used_monsters is not None:
        data["used_monsters"] = used_monsters
    if max_inv_size is not None:
        data["max_inv_size"] = max_inv_size
    data["player"]["weapons_inv"] = {}

    for n, weapon in enumerate(new_player.weapons):
        data["player"]["weapons_inv"][f"weapon_slot_{n+1}"]={
            "name": weapon.name,
            "power": weapon.power,
            "stim": weapon.stim,
            "mana": weapon.mana,
            "buff_count": weapon.buff_count
        }

    data["player"]["objects_inv"] = {}
    for n, obj in enumerate(new_player.inventory):
        data["player"]["objects_inv"][f"object_slot_{n+1}"]={
            "name": obj.name,
            "effect": obj.effect,
            "value": obj.value
        }

    with open("JSON/active_data.json", "w", encoding="utf-8") as write_file:
        json.dump(data, write_file, indent=4, ensure_ascii=False)

def saved_game():
    return data["player"]["nickname"] is not None and data["player"]["pv"] > 0 and data["player"]["max_pv"] is not None and data["player"]["stim"] is not None

def get_save():
    if saved_game():
        return {
            "nickname": data["player"]["nickname"],
            "level": data["player"].get("current_level", 1),
            "pv": data["player"]["pv"],
            "max_pv": data["player"]["max_pv"],
            "score": data["player"].get("score", 0)
        }
    return None

def clear_save():
    global data # Le temps que j'ai mis à trouver ça ¯\_(ツ)_/¯

    data = {
        "player": {
            "nickname": None,
            "pv": None,
            "max_pv": None,
            "stim": None,
            "max_stim": None,
            "mana": None,
            "max_mana": None,
            "score": None,
            "current_level": None,
            "weapons_inv": {},
            "objects_inv": {}
        },
        "used_monsters": [],
        "cheat": False,
        "seed": None
    }

    with open("JSON/active_data.json", "w", encoding="utf-8") as write_file:
        json.dump(data, write_file, indent=4, ensure_ascii=False)


def get_player_data():
    weapons_inventory = []
    for i in data["player"]["weapons_inv"].keys():
        a = data["player"]["weapons_inv"][i]["name"]
        b = data["player"]["weapons_inv"][i]["power"]
        c = data["player"]["weapons_inv"][i]["stim"]
        d = data["player"]["weapons_inv"][i]["mana"]
        e = data["player"]["weapons_inv"][i].get("buff_count", 0)
        weapons_inventory.append(Weapon(a, b, c, d, e))

    objects_inventory = []
    for i in data["player"]["objects_inv"].keys():
        a = data["player"]["objects_inv"][i]["name"]
        b = data["player"]["objects_inv"][i]["effect"]
        c = data["player"]["objects_inv"][i]["value"]
        objects_inventory.append(Object(a,b,c))

    return Player(data["player"]["nickname"],
            data["player"]["pv"],
            data["player"]["max_pv"],
            data["player"]["stim"],
            data["player"]["max_stim"],
            data["player"]["mana"],
            data["player"]["max_mana"],
            weapons_inventory,
            objects_inventory)

def get_used_monsters():
    return data.get("used_monsters", [])

