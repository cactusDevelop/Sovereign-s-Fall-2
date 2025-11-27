
import os, time

from global_func import get_width, clear_console
from musics import play_sound
from constants import ULT_COEFFICIENT, RED, CYAN, RESET


class Character:
    def __init__(self, name: str, pv: int, max_pv:int):
        self.name = name
        self.pv = pv
        self.max_pv = max_pv
        self.weapon = None

    def attack(self, target):
        if hasattr(target, "calc_dmg"):
            return target.calc_dmg(self.weapon.power, self.weapon.name)
        else:
            old_pv = target.pv
            target.pv = max(target.pv - int(self.weapon.power*target.nerf_defense), 0)
            overkill = 0
            if target.pv == 0:
                overkill = int(self.weapon.power*target.nerf_defense)-old_pv

            print(f"""Arme "{CYAN + self.weapon.name + RESET}" inflige {self.weapon.power} dégats à "{RED + target.name + RESET}" ({target.pv} PV restants)""")
            return overkill


def show_ult_animation():
    play_sound("sword-combo")

    if not os.path.exists("ascii-frames.txt"):
        print("[Animation non disponible]")
        return

    try:
        with open("ascii-frames.txt", "r", encoding="utf-8") as f:
            content = f.read()

        frames = content.split(",\n")

        try:
            max_height = os.get_terminal_size().lines - 2
        except OSError:
            max_height = 24

        for frame in frames:

            lines = frame.split('\n')
            lines_to_display = lines[:max_height]

            for line in lines_to_display:
                print(line[:get_width() - 2])

            time.sleep(0.05)
            clear_console()

    except Exception as e:
        print(f"[Erreur animation: {e}]")
        return


class Player(Character):
    def __init__(self, name:str, pv:int, max_pv:int, stim:int, max_stim:int, mana:int, max_mana:int, weapons:list, inventory:list):
        super().__init__(name, pv, max_pv)
        self.stim = stim
        self.max_stim = max_stim
        self.mana = mana
        self.max_mana = max_mana
        self.weapons = weapons
        self.inventory = inventory
        self.shield_pv = 0
        self.can_ult = (self.stim == self.max_stim)

    def charge(self, x):
        self.stim = min(self.stim+x, self.max_stim)
        self.can_ult = (self.stim == self.max_stim)

    def mana_ult_charge(self, x):
        self.mana = min(self.mana + x, self.max_mana)
        self.stim = min(self.stim + 10*x, self.max_stim)

    def ult(self, target):
        if self.can_ult:
            show_ult_animation()

            powers = [weapon.power for weapon in self.weapons]
            geo = 1
            for p in powers:
                geo *= max(p,1)
            geo = geo**(1/len(powers))
            ari = sum(powers) / len(powers)

            dgt = int((0.7*geo+0.3*ari)*ULT_COEFFICIENT*target.nerf_defense)

            old_pv = target.pv
            target.pv = max((target.pv - dgt), 0)
            overkill = 0
            if target.pv == 0:
                overkill = dgt - old_pv

            print(f"\nVos armes s'unissent et attaquent de {dgt} dégats !")

            self.can_ult = False
            self.stim = 0
            return overkill
        else:
            return "[DEBUG] NE PEUT PAS ULT"

    def heal(self, x):
        self.pv = min(self.pv+x, self.max_pv)

    def use_obj(self, obj_position, max_inv_size, lvl):
        if 0 <= obj_position < len(self.inventory):
            obj = self.inventory[obj_position]

            if obj.effect == "new_obj" and len(self.inventory) >= max_inv_size:
                print("Inventaire plein...")
                return False
            else:
                check = obj.use(self, max_inv_size, lvl)
                if obj.effect != "new_obj" and check:
                    self.inventory.pop(obj_position)
                return True if check is not False else False
        else:
            print("[DEBUG] Pas d'objet")
            return False

    def shield(self, s_pv):
        self.shield_pv = max(self.shield_pv, s_pv) # Bouclier fort écrase bouclier faible
        print(f"Bouclier de {self.shield_pv} Pv actif")

    def calc_dmg(self, damage, weapon_name="Attaque ennemie"):
        if self.shield_pv > 0:
            if damage >= self.shield_pv:
                self.shield_pv = 0
                print(f"""Arme "{RED + weapon_name + RESET}" détruit votre Bouclier""")
                play_sound("drop-shield")
            else:
                self.shield_pv = self.shield_pv - damage
                print(f"""Arme "{RED + weapon_name + RESET}" inflige {damage} dégats au bouclier ({CYAN + str(self.shield_pv) + RESET} PV bouclier restants)""")
                play_sound("shield")

        else:
            self.pv = max(self.pv - damage, 0)
            print(f"""Arme "{RED + weapon_name + RESET}" inflige {damage} dégats à "{CYAN + self.name + RESET}" ({self.pv} PV restants)""")
            play_sound("monster-attack")


class Monster(Character):
    def __init__(self, name: str, pv: int, weapon, weakness=0):
        super().__init__(name, pv, pv)
        self.weapon = weapon
        self.weakness = weakness
        self.nerf_defense = 1.0
