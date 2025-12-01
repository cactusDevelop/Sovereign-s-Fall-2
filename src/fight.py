
import random

from global_func import *
from musics import play_sound, stop_sound
from constants import (MAX_ANALYSIS, WEAKNESSES, MAX_INV_SIZE, FADE_OUT, MISS_CHANCE, HEAL_CHANCE, HEAL_AMOUNT,
                       MAX_NAV_ITERATIONS, RED, BLUE, CYAN, GREY, GOLD, RESET)


class Fight:
    def __init__(self, player, enemy, level=0, max_analysis=MAX_ANALYSIS, tuto=False):
        self.player = player
        self.enemy = enemy
        self.turn_count = 0
        self.weakness_turns_remaining = 0
        self.analysis_count = max_analysis
        self.max_analysis = max_analysis
        self.level = level
        self.tuto = tuto


    def fight_loop(self, max_inv_size=MAX_INV_SIZE, boss_music=False):
        print(f"\n{CYAN + self.player.name + RESET} engage le combat contre {RED}{self.enemy.name + RESET}")
        wait_input()
        if boss_music:
            play_sound("boss", True)
        else:
            play_sound("fight", True)

        while True:
            self.turn_count += 1

            self.weakness_turns_remaining = max(self.weakness_turns_remaining - 1, 0)

            p_turn_conclu, overkill = self.player_turn(max_inv_size)
            if p_turn_conclu == "Att":
                play_sound("sword-sound")
            elif p_turn_conclu == "Obj":
                play_sound("bell")
            elif p_turn_conclu == "Ana":
                play_sound("bell")
            elif p_turn_conclu == "Pass":
                play_sound("hmm")
            elif p_turn_conclu == "gameover2":
                return "gameover2"
            elif p_turn_conclu is None:
                continue

            gagne = self.check_end()
            if gagne and p_turn_conclu == "Att" and overkill:
                stop_sound(FADE_OUT)
                play_sound("sword-finish")
                time.sleep(1)
                play_sound("win")
                wait_input()
                return gagne, overkill
            elif gagne and p_turn_conclu != "Att":
                stop_sound(FADE_OUT)
                play_sound("win")
                wait_input()
                return gagne


            self.enemy_turn()
            gagne = self.check_end()
            if gagne is False:
                stop_sound(FADE_OUT)
                time.sleep(1)
                play_sound("laughter")
                time.sleep(FADE_OUT/1000-1)
                return gagne



    def player_turn(self, max_inv_size=MAX_INV_SIZE):
        instruction, value = self.nav(self.player, max_inv_size)

        if instruction == "Armes":
            equiped_w = self.player.weapons[value]
            self.player.weapon = equiped_w

            if self.player.mana < equiped_w.mana:
                return None, None

            self.player.mana -= equiped_w.mana

            overkill = self.player.attack(self.enemy)
            if overkill > 0:
                return "Att", overkill

            self.player.charge(self.player.weapon.stim)

            self.player.mana = min(self.player.mana + 1, self.player.max_mana)
            return "Att", None

        elif instruction == "Objets":
            obj = self.player.inventory[value]
            if obj.effect == "new_obj":
                if self.player.mana < 3:
                    print("Mana insuffisant")
                    wait_input()
                    return None, None
                elif len(self.player.inventory) >= max_inv_size:
                    print("Inventaire plein")
                    wait_input()
                    return None, None

            action_check = self.player.use_obj(value, max_inv_size, self.level)
            if action_check:
                self.player.mana = min(self.player.mana + 1, self.player.max_mana)
                return "Obj", None
            else:
                return None, None

        elif instruction == "Analyse":
            if self.analysis_count <= 0:
                print("[DEBUG] Mana insuffisant déjà annoncé")
                wait_input()
                return None, None

            self.analysis_count -= 1

            print(f"\nMeilleure compréhension : {self.find_weakness()}")

            self.player.mana = min(self.player.mana + 1, self.player.max_mana)
            return "Ana", None

        elif instruction == "Ultime":
            print("\nLa volonté des dieux vous accompagnent...")
            self.player.ult(self.enemy)

            self.player.mana = min(self.player.mana + 1, self.player.max_mana)
            return "Ult", None

        elif instruction == "Passer":
            print("\nImpuissant, vous passez votre tour")
            self.player.mana = min(self.player.mana + 1, self.player.max_mana)
            return "Pass", None

        elif instruction == "sus":
            return "gameover2", None

        else:
            return None, None


    def enemy_turn(self):
        print("\n" +"=" * 5 + f"| {RED}" + self.enemy.name + "'s turn" + f"{RESET} |" + "=" * (get_width() - 16 - len(self.enemy.name)))
        print()

        if random.random() < MISS_CHANCE or self.enemy.weapon.power == 0:
            play_sound("miss-swing")
            print(f""""{RED + self.enemy.name + RESET}" rate lamentablement son attaque""")

        elif random.random() < HEAL_CHANCE:
            self.enemy.pv = min(self.enemy.pv + int(self.enemy.max_pv*HEAL_AMOUNT), self.enemy.max_pv)
            play_sound("heal")
            print(f""""{RED + self.enemy.name + RESET}" se régène partiellement""")

        else:
            self.enemy.attack(self.player)

        input("Continuer...")
        clear_console()
        self.display_status()



    def check_end(self):
        if self.enemy.pv <= 0:
            print("\n VICTOIRE !!!")
            return True

        elif self.player.pv <= 0:
            print("\n Votre corps ne vous répond plus")
            return False

        return None


    def display_status(self):
        p_pv_ratio = self.player.pv * 10 // self.player.max_pv
        p_stim_ratio = self.player.stim * 10 // self.player.max_stim
        e_pv_ratio = self.enemy.pv * 10 // self.enemy.max_pv
        p_mana_ratio = self.player.mana * 10 // self.player.max_mana
        p_shield_ratio = self.player.shield_pv * 10 // self.player.max_pv
        left_offset = 2

        pv_bar = ""
        for i in range(10):
            if i < p_shield_ratio and i <= p_pv_ratio:
                pv_bar += BLUE + "█" + RESET
            elif i < p_pv_ratio:
                pv_bar += "█"
            elif p_pv_ratio < i < p_shield_ratio:
                pv_bar += BLUE + "▄" + RESET
            else:
                pv_bar += "_"

        line_0 = f"\n NIVEAU {self.level}"

        line_1 = "=" * 5 + f"| {CYAN}" + self.player.name + "'s turn" + f"{RESET} |" + "=" * (get_width() - 16 - len(self.player.name))

        line_2 = " " * left_offset + CYAN + self.player.name.upper() + RESET + " " * (get_width() // 2 - len(self.player.name))
        line_2 += RED + "FRAGMENTUS " + self.enemy.name.upper() + RESET

        line_3 = " "*left_offset + pv_bar + " | " + str(self.player.pv) + "/" + str(self.player.max_pv) +" PV"
        if self.player.shield_pv > 0:
            line_3 += f" [Bouclier {self.player.shield_pv}PV]"
        visible_length = len(line_3) - line_3.count(BLUE) * len(BLUE) - line_3.count(RESET) * len(RESET)
        line_3 += " " * (get_width()//2 - visible_length + left_offset)
        line_3 += "█"*e_pv_ratio + "_"*(10-e_pv_ratio) + " | " + str(self.enemy.pv) + "/" + str(self.enemy.max_pv) +" PV"

        line_4 = " "*left_offset + "█"*p_stim_ratio + "_"*(10-p_stim_ratio) + " | " + str(self.player.stim) + "/" + str(self.player.max_stim) +" ULT"

        line_5 = " "*left_offset + "█"*p_mana_ratio + "_"*(10-p_mana_ratio) + " | " + str(self.player.mana) + "/" + str(self.player.max_mana) +" MANA"

        print(line_0)
        print(line_1)
        print()
        print(line_2)
        print(line_3)
        print(line_4)
        print(line_5)

        if self.weakness_turns_remaining > 0:
            print(" "*left_offset + f" -Analyse actif pour {self.weakness_turns_remaining} tour(s)")
        else:
            self.enemy.weapon.power = self.enemy.weapon.original_power
            self.enemy.nerf_defense = 1.0
        print()

    def find_weakness(self):
        weakness = str(self.enemy.weakness)

        if weakness == "0" or weakness not in WEAKNESSES:
            return "Que dalle"

        weakness_data = WEAKNESSES[weakness]
        w_type = weakness_data["type"]
        w_value = weakness_data["value"]
        w_duration = weakness_data["duration"]
        w_message = weakness_data["message"]

        if w_type == "attack":
            self.enemy.weapon.power = max(self.enemy.weapon.power - int(self.enemy.weapon.original_power*(w_value/100)), 0)
            self.weakness_turns_remaining = w_duration + 1
            return w_message

        elif w_type == "heal":
            self.player.heal(self.player.pv*w_value//100)
            play_sound("heal")
            print(f"L'ennemi vous guérit de {self.player.pv*w_value//100} PV ?!")
            return w_message

        elif w_type == "defense":
            self.enemy.nerf_defense = w_value
            self.weakness_turns_remaining = w_duration + 1
            return w_message

        else:
            return "[DEBUG] Big Error : la faiblesse n'existe pas"


    def nav(self, player, max_inv_size=MAX_INV_SIZE):
        can_att = any(i.mana <= player.mana for i in player.weapons)
        can_obj = len(player.inventory) > 1
        can_sac = player.mana > 2 and len(player.inventory) < MAX_INV_SIZE
        can_ana = self.analysis_count > 0

        can_play = can_att or can_obj or can_sac or can_ana or player.can_ult
        nav_menu = ["Armes", "Objets", "Analyse"]

        if player.can_ult:
            nav_menu.append("Ultime")
        elif not can_play:
            nav_menu.append("Passer")

        if self.tuto:
            nav_menu.append("Info")

        current_pos = "Nav"

        for it in range(MAX_NAV_ITERATIONS):

            if current_pos not in ["Analyse", "Ultime", "Passer"]:
                clear_console()

            if current_pos == "Nav":
                def to_display():
                    self.display_status()

                    print("=" * 10 + "Menu" + "=" * 10)
                    for i, option in enumerate(nav_menu):
                        is_disabled = False
                        if option == "Armes" and not can_att:
                            is_disabled = True
                        elif option == "Objets" and not can_obj and not can_sac:
                            is_disabled = True
                        elif option == "Analyse" and not can_ana:
                            is_disabled = True

                        if is_disabled:
                            if option == "Analyse":
                                print(f"{GREY}[{i + 1}] {option} ({self.analysis_count}/{self.max_analysis}){RESET}")
                            elif option == "Objets":
                                print(f"{GREY}[{i + 1}] {option} ({len(player.inventory)}/{max_inv_size}){RESET}")
                            else:
                                print(f"{GREY}[{i + 1}] {option}{RESET}")
                        else:
                            if option == "Analyse":
                                print(f"[{i + 1}] {option} ({self.analysis_count}/{self.max_analysis})")
                            elif option == "Objets":
                                print(f"[{i + 1}] {option} ({len(player.inventory)}/{max_inv_size})")
                            else:
                                print(f"[{i + 1}] {option}")

                def conf(action_input):
                    return action_input.isdigit() and 0 < int(action_input) <= len(nav_menu)

                action = int(solid_input(conf,to_display)) - 1
                selected_option = nav_menu[action]

                if selected_option == "Armes" and not can_att:
                    print("Aucune arme utilisable")
                    wait_input()
                    continue
                elif selected_option == "Objets" and not can_obj and not can_sac:
                    print("Aucun objet utilisable")
                    wait_input()
                    continue
                elif selected_option == "Analyse" and not can_ana:
                    print("T'as trop spam la passivité mon gars")
                    wait_input()
                    continue

                current_pos = selected_option

            elif current_pos == "Armes":
                def to_display():
                    self.display_status()
                    print("="*15 + "Armes" + "="*15)

                    max_len = max(len(w.name.replace(GOLD, '').replace(RESET, '')) for w in player.weapons)

                    for i, option in enumerate(player.weapons):
                        clean_name = option.name.replace(GOLD, '').replace(RESET, '')
                        offset = " " * (max_len + 2 - len(clean_name))

                        enough_mana = player.mana >= option.mana

                        if GOLD in option.name:
                            display_name = f"{GOLD}{clean_name}{RESET}"
                        elif not enough_mana:
                            display_name = f"{GREY}{clean_name}{RESET}"
                        else:
                            display_name = clean_name

                        display_stats = f"(Att:{option.power}, Ult:{option.stim}, Mana:{option.mana})"
                        if not enough_mana:
                            display_stats = f"{GREY}{display_stats}{RESET}"

                        print(f"[{i + 1}] {display_name + offset + display_stats}")
                    print(f"[{len(player.weapons) + 1}] Retour")
                def conf(action_input):
                    return action_input.isdigit() and 0 < int(action_input) <= len(player.weapons)+1

                action = int(solid_input(conf, to_display))-1

                if action == len(player.weapons):
                    current_pos = "Nav"
                elif player.mana < player.weapons[action].mana:
                    print(f"Mana insuffisant ({player.mana}/{player.weapons[action].mana})")
                    wait_input()
                    return "Armes", action
                else:
                    return "Armes", action

            elif current_pos == "Objets":
                def to_display():
                    self.display_status()
                    print("=" * 10 + "Objets" + "=" * 10)

                    for i, option in enumerate(player.inventory):
                        effect = "Objet généré aléatoirement pour 3 MANA" if option.effect == "new_obj" \
                            else f"Soin de {option.value} PV" if option.effect == "heal" \
                            else f"Arme améliorée de {option.value} Att" if option.effect == "att_boost" \
                            else f"Bouclier de {option.value} PV" if option.effect == "shield" \
                            else f"Charge de {option.value} MANA" if option.effect == "mana_ult_charge" \
                            else f"Arme x{option.value} Att" if option.effect == "att_mult" \
                            else "[DEBUG] Effet défaillant"

                        max_len = max(len(o.name) for o in player.inventory)
                        index_prefix = " " if (i < 9 and len(player.inventory) >= 10) else ""
                        offset = " " * (max_len + 2 - len(option.name))
                        print(f"{index_prefix}[{i + 1}] {option.name}{offset}(Effet: {effect})")

                    retour_prefix = " " if len(player.inventory) >= 9 else ""
                    print(f"{retour_prefix}[{len(player.inventory) + 1}] Retour")
                def conf(action_input):
                    return action_input.isdigit() and 0 < int(action_input) <= len(player.inventory)+1

                action = int(solid_input(conf, to_display))-1

                if action == len(player.inventory):
                    current_pos = "Nav"
                else:
                    return "Objets", action

            elif current_pos == "Analyse":
                return "Analyse", 0

            elif current_pos == "Ultime":
                return "Ultime", 0

            elif current_pos == "Passer":
                return "Passer", 0

            elif current_pos == "Info":
                print("=" * 10 + "Vaincre des Fragmentus" + "=" * 10)
                typew_print((
                    "\nA chaque tour, vous pouvez exécuter une action :",
                    "\n",
                    "\n  1. Attaquer avec une arme en payant du mana.",
                    "\n     Les attaques infligent des dégats et/ou chargent votre Ultime.",
                    "\n     Tous les 5 niveaux, le joueur a la possiblité de recupérer une arme",
                    "\n     plus efficace sur la carcasse d'un Boss."
                    "\n",
                    "\n  2. Utiliser un objet.",
                    "\n     Seul le sac des abîmes coûte du mana pour l'utiliser mais en contrepartie",
                    "\n     il génère aléatoirement un objet qui n'est pas déjà dans l'inventaire.",
                    "\n     La taille de l'inventaire est fixée à 6.",
                    "\n     A la fin de chaque combat vous recevrez un objet aléatoire s'il y a assez",
                    "\n     de place dans votre inventaire."
                    "\n     Les objets générés sont de plus en plus puissants avec les niveaux."
                    "\n",
                    "\n  3. Analyser l'ennemi.",
                    "\n     Cette action expose une de ses faiblesses... ou pas",
                    "\n",
                    "\n  4. Ultime",
                    "\n     Apparait lorsque la jauge d'Ult est complètement chargée."
                    "\n     Attaque surpuissante qui est calculée comme une moyenne géométrique",
                    "\n     de la puissance de toutes vos armes, fois un facteur multiplicatif.",
                    "\n     Malheureusement la jauge d'Ult augmente à chaque niveau, ce qui",
                    "\n     oblige le joueur à renouveler ses armes psychiques.",
                    "\n",
                    "\n  5. Passer",
                    "\n     Dans le cas très rare où aucune autre action n'est possible... passez."
                ))

                wait_input()
                current_pos = "Nav"

        print("Arrête de naviguer sans rien faire, reviens quand tu sauras prendre des décisions")
        return "sus", None

