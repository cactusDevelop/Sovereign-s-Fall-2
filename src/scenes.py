
import random

from json_manager import get_cst_names, save_hs, clear_save
from weapon import Weapon, generate_starters, gen_boss_weapon
from musics import play_sound, stop_sound
from characters import Monster
from object import Object, get_rand_obj
from fight import Fight
from global_func import *
from firebase_hs import save_score_with_fallback
from constants import (INCOGNITO, MAX_ANALYSIS, MAX_INV_SIZE, MAX_WEAPON_SLOTS, PLAYER_I_PV, PLAYER_I_MANA, PLAYER_I_ULT,
                       PLAYER_SCALE, PLAYER_ULT_SCALE, PLAYER_MANA_SCALE, MONSTER_I_PV, MONSTER_I_POWER, MONSTER_SCALE,
                       BOSS_I_PV, BOSS_I_POWER, BOSS_SCALE, RANDOM_LINES, WEAKNESSES, REV_WHITE, REV_B_W, RED, GREEN,
                       BLUE, CYAN, BOLD, RESET)

OBJ_STARTER = Object("Sac des abîmes", "new_obj", 0)
CHEAT_WEAPON = Weapon("Mange tes morts", 9999, 9999, 0, 0)
MAX_NAME_SIZE = get_width()//3


def clean_nick(nickname):
    nickname = nickname.strip()
    if not nickname:
        return f"Joueur{random.randint(1, 99)}"
    if len(nickname) > MAX_NAME_SIZE:
        return nickname[:MAX_NAME_SIZE-3]+"..."
    return nickname

def choose_starter(s_list):
    def to_display():
        left_offset = 8
        for j in s_list:
            print(f"[{s_list.index(j) + 1}] {j.name}:" + " "*(left_offset-len(j.name)) + f"Power {j.power}, Ult Charge {j.stim}, Mana {j.mana}")
    def conf(action_input):
        return action_input.isdigit() and 0 < int(action_input) <= len(s_list)

    choice = solid_input(conf, to_display)
    return s_list[int(choice)-1]

def game_over(data,x:int,des:str):
    clear_console()
    stop_sound(1000)

    seed = data["seed"]
    nickname = data["player"]["nickname"]
    score = data["player"]["score"]
    level = data["player"]["current_level"]
    is_cheating = data.get("cheat", False)

    test_high = False
    if score > 0 and not is_cheating:
        new_hs = save_score_with_fallback(nickname, score, level, save_hs)
        test_high = (score == new_hs)

    print(f"\n{REV_WHITE}" + "=" * get_width())
    print(f"  {REV_B_W}GAME OVER{REV_WHITE}" + " " * (get_width() - 11))
    print(f"  Fin {x} - {des}" + " " * (get_width()-9-len(str(x))-len(des)))
    print(f"  Score - {score}" + " " * (get_width()-9-len(str(x))-len(str(score))))
    print(f"  Seed - {seed}" + " "*(get_width()-9-len(str(seed))))
    if is_cheating:
        print("  Pas de gloire aux tricheurs, score perdu !" + " "*(get_width()-45))
    if test_high:
        print(f" >>> NEW HIGHSCORE <<<" + " "*(get_width()-22))
    print(" " * get_width() + "\n" + " " * get_width())
    print("=" * get_width() + RESET)

    clear_save()
    input("\nAppuyez sur ENTER pour revenir à l'écran d'accueil")
    return False


# SCENES
def launch_cutscene(data):
    clear_console()
    stop_sound(1500)
    time.sleep(1.7)
    play_sound("tense-bgm", True)

    seed = data.get("seed")

    print((
        f"\n{GREEN}"
        "\n *sauvegarde auto*"
        f"\n seed : {seed}"
        "\n"
        "\n          ⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷"
        "\n   ⠀⠀⠀⠀ ⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿"
        "\n   ⠀⠀⠀⠀⠀ ⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿"
        "\n   ⠀⣠⣤⣤⣤⣤⣴⣿⣿⣿⣿⣿⣿⡟⠛⠛⣿⣿⣿⣿⣿⣿⣿"
        "\n   ⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⣿⣿⣿⣿⣿⣿⣿"
        "\n   ⣿⣿⣿⣿⣿⣿⣿⠟⢹⣿⣿⣿⣿⡇⠀⠀⣿⣿⣿⣿⣿⣿⣿"
        "\n   ⣿⣿⣿⣿⣿⠟⠁⠀⠸⠿⠿⠿⠿⠃⠀⢀⣿⣿⣿⣿⣿⣿⣿"
        "\n   ⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣾⣿⣿⣿⣿⣿⣿⣿"
        "\n   ⣿⣿⣿⣿⣿⣷⣄⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿"
        "\n   ⣿⣿⣿⣿⣿⣿⣿⣷⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿"
        "\n   ⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿"
        "\n"
        f"\n   Pour continuer : Appuyer sur -> {BOLD}ENTER <- {RESET}"))
    wait_input()

    play_sound("intro")
    title = center_txt((
        f"{BLUE}\n",
        "\n",
        "\n",
        "\n",
        "  ██████  ▒█████   ██▒   █▓▓█████  ██▀███  ▓█████  ██▓  ▄████  ███▄    █   ██████      █████▒▄▄▄       ██▓     ██▓    ",
        "▒██    ▒ ▒██▒  ██▒▓██░   █▒▓█   ▀ ▓██ ▒ ██▒▓█   ▀ ▓██▒ ██▒ ▀█▒ ██ ▀█   █ ▒██    ▒    ▓██   ▒▒████▄    ▓██▒    ▓██▒    ",
        "░ ▓██▄   ▒██░  ██▒ ▓██  █▒░▒███   ▓██ ░▄█ ▒▒███   ▒██▒▒██░▄▄▄░▓██  ▀█ ██▒░ ▓██▄      ▒████ ░▒██  ▀█▄  ▒██░    ▒██░    ",
        "  ▒   ██▒▒██   ██░  ▒██ █░░▒▓█  ▄ ▒██▀▀█▄  ▒▓█  ▄ ░██░░▓█  ██▓▓██▒  ▐▌██▒  ▒   ██▒   ░▓█▒  ░░██▄▄▄▄██ ▒██░    ▒██░    ",
        "▒██████▒▒░ ████▓▒░   ▒▀█░  ░▒████▒░██▓ ▒██▒░▒████▒░██░░▒▓███▀▒▒██░   ▓██░▒██████▒▒   ░▒█░    ▓█   ▓██▒░██████▒░██████▒",
        "▒ ▒▓▒ ▒ ░░ ▒░▒░▒░    ░ ▐░  ░░ ▒░ ░░ ▒▓ ░▒▓░░░ ▒░ ░░▓   ░▒   ▒ ░ ▒░   ▒ ▒ ▒ ▒▓▒ ▒ ░    ▒ ░    ▒▒   ▓▒█░░ ▒░▓  ░░ ▒░▓  ░",
        "░ ░▒  ░ ░  ░ ▒ ▒░    ░ ░░   ░ ░  ░  ░▒ ░ ▒░ ░ ░  ░ ▒ ░  ░   ░ ░ ░░   ░ ▒░░ ░▒  ░ ░    ░       ▒   ▒▒ ░░ ░ ▒  ░░ ░ ▒  ░",
        "░  ░  ░  ░ ░ ░ ▒       ░░     ░     ░░   ░    ░    ▒ ░░ ░   ░    ░   ░ ░ ░  ░  ░      ░ ░     ░   ▒     ░ ░     ░ ░   ",
        "      ░      ░ ░        ░     ░  ░   ░        ░  ░ ░        ░          ░       ░                  ░  ░    ░  ░    ░  ░",
        "                       ░                                                                                              ",
        "\n",
        RESET))
    typew_print(title)
    wait_input()

    clear_console()
    play_sound("wood-creak")
    quick_print((
        "\nVous vous réveillez dans un pièce sombre qui vous est inconnue.",
        "\nUn homme tout de noir vêtu vous tend un parchemin.",
        f"\n\n{INCOGNITO} : « Complétez ceci »"))

    print()
    play_sound("paper-collect")
    typew_print(center_txt((
        " _________________________________________________________________ ",
        "|                                                                 |",
        "|                                                                 |",
        "|   Vous avez eu l’exceptionnellement incroyable chance           |",
        "|   d’être sélectionné pour prendre part au programme *XXXXX*.    |",
        "|                                                                 |")))
    wait_input()
    play_sound("paper-rustle")
    typew_print(center_txt((
        "|                                                                 |",
        "|   - Toute atteinte à la sécurité du participant durant le       |",
        "|   programme relève de son entière responsabilité.               |",
        "|   - Le participant n’est pas autorisé à interrompre le          |",
        "|   programme avant la fin.                                       |")))
    wait_input()
    play_sound("paper-rustle")
    typew_print(center_txt((
        "|                                                                 |",
        "|   Je soussigné (nom, prénom)...............................     |",
        "|   accepte en toute connaissance de cause, les conditions        |",
        "|   présentées cfr supra.                                         |",
        "|                                                                 |",
        "|_________________________________________________________________|")))

    print(f"\n{INCOGNITO} : « Avez-vous lu et accepté ce contrat » ")

    def to_display():
        print(f"\n{INCOGNITO} : « Nous réitérons notre demande... »")
        print(f"{INCOGNITO} : « Acceptez-vous ce contrat » (oui/non)")
        play_sound("hmm")
    def conf(action_input):
        return action_input.lower() in ["oui", "non"]

    agreement = input(" > ").strip().lower()
    if agreement != "oui" and agreement != "non":
        agreement = solid_input(conf,to_display)

    if agreement.lower() == "non":
        pseudo = clean_nick(input(f"\nPseudo > {CYAN}"))
        data["player"]["nickname"] = pseudo

        print(f"\n {CYAN + pseudo + RESET} : « Va te faire foutre. »")
        wait_input()
        play_sound("laughter")
        print(f"{INCOGNITO} : « Pensez-vous avoir le choix ? »")
        time.sleep(2)
        return False

    else:
        pseudo = clean_nick(input(f"\nSignature (pseudo) > {CYAN}"))
        play_sound("handwriting")
        play_sound("door-shut")
        data["player"]["nickname"] = pseudo

        quick_print((
            f"\n{RESET}Il vous voile les yeux de force. Vous entendez le claquement sourd d'une porte métallique.",
            "\nUne nausée commence à vous prendre... Votre tête brule... Vos tympans bourdonnent...",
            "\nVous vous sentez tel un Ampèremètre branché en parallèle...",
            "\nEt vous perdez connaissance."))
        print()
        print("...")
        play_sound("teleport")
        time.sleep(1)

        return True


def launch_starters_scene(data):
    clear_console()
    starters = generate_starters()
    nickname = data["player"]["nickname"]

    quick_print((
                f"\n {CYAN + nickname + RESET} : « ... Qu’est-ce que... Où suis-je tombé ? »",
                "\n\nDevant vous, se trouvent plusieurs armes difformes éparpillées sur le sol.",
                f"\n\n{INCOGNITO} : « Bienvenue dans la tête du Roi, agent {nickname} »",
                f"\n{INCOGNITO} : « Votre objectif sera de le {RED}TuER{RESET} »",
                f"\n{INCOGNITO} : « Pour ce faire, détruisez les fragments de son esprit que vous rencontrerez »",
                f"\n{INCOGNITO} : « Choisissez une arme. »"))

    print("\n")
    weapon_slot_1 = choose_starter(starters)
    starters.remove(weapon_slot_1)
    play_sound("bell")

    quick_print((f"\n{INCOGNITO} : « Ah, j'ai oublié de préciser que vous pourrez faire une attaque combinée... »",
                f"\n{INCOGNITO} : « Donc vous aurez besoin de deux autres armes supplémentaires. »"))

    print("\n\n <2e arme>")
    weapon_slot_2 = choose_starter(starters)
    starters.remove(weapon_slot_2)
    play_sound("bell")

    print("\n <3e arme>")
    weapon_slot_3 = choose_starter(starters)
    starters.remove(weapon_slot_3)
    play_sound("bell")

    quick_print((f"\n{INCOGNITO} : « Je te donne un dernier objet : un sac dans lequel tu devras mettre tes trouvailles »",
               f"\n{INCOGNITO} : « Tu n'es pas le premier à t'en servir c'est pour ça qu'il y a quelques déchets dedans »"))
    play_sound("bell")
    data["player"]["objects_inv"] =  {"object_slot_1":{"name": OBJ_STARTER.name, "effect": OBJ_STARTER.effect, "value": OBJ_STARTER.value}}

    selected_weapons = [weapon_slot_1,weapon_slot_2,weapon_slot_3]

    if data.get("cheat", False):
        print(f"\n{INCOGNITO} : « Tiens tiens tiens... tu as triché ? Bah tiens chacal »")
        wait_input()

        selected_weapons.append(CHEAT_WEAPON)
        play_sound("bell")
        print(f""" > Arme "{CHEAT_WEAPON.name}" récupérée""")
        print()

    for n, weapon in enumerate(selected_weapons):
        data["player"]["weapons_inv"][f"weapon_slot_{n+1}"]={
            "name": weapon.name,
            "power": weapon.power,
            "stim": weapon.stim,
            "mana": weapon.mana
        }


    # DEFAULT STATS
    data["player"]["pv"] = data["player"]["max_pv"] = 100
    data["player"]["stim"] = 100
    data["player"]["max_stim"] = 200
    data["player"]["mana"] = data["player"]["max_mana"] = 10

    stop_sound(2000)

    print(f"\n{INCOGNITO} : « Attention un fragment a été repéré ! »")
    wait_input()

def launch_tuto_fight(player):
    tuto_enemy = Monster("Tuto", 200, Weapon("Épée classique", 10, 0, 0, 0), 1)
    result = Fight(player, tuto_enemy, 0, 1, True).fight_loop()
    return result

def launch_keep_fighting(difficulty, player, used_monsters, max_analysis=MAX_ANALYSIS, max_inv_size=MAX_INV_SIZE, max_weapon_slots=MAX_WEAPON_SLOTS):
    clear_console()
    stop_sound(1000)

    MONSTER_NAMES, BOSS_NAMES, WEAPON_NAMES = get_cst_names()
    is_bossfight = (difficulty % 5 == 0 and difficulty != 0)

    if is_bossfight:
        print("\nBoss puissant en approche !")
        print(f"Attention ! La puissance du boss affecte votre régénération.")
        boss_name = f"BOSS {random.choice(BOSS_NAMES).upper()}"

        boss_pv = int(BOSS_I_PV*BOSS_SCALE**difficulty)
        boss_power = int(BOSS_I_POWER*BOSS_SCALE**difficulty)

        boss_weapon = Weapon("Arme très puissante", boss_power, 0, 0, 0)
        new_enemy = Monster(boss_name, boss_pv, boss_weapon, 0)

        player.max_pv = int(PLAYER_I_PV * PLAYER_SCALE**difficulty)
        player.max_stim = int(PLAYER_I_ULT * PLAYER_ULT_SCALE**difficulty)
        player.max_mana = int(PLAYER_I_MANA * PLAYER_MANA_SCALE**difficulty)
        player.can_ult = (player.stim >= player.max_stim)
        player.pv = int(player.max_pv//(4/3))
        player.mana = player.max_mana//2
        fight_result = Fight(player, new_enemy, difficulty, max_analysis, False).fight_loop(max_inv_size, True)

    else:
        print()
        print(random.choice(RANDOM_LINES))

        available_enemies = []
        for i in MONSTER_NAMES:
            if i not in used_monsters:
                available_enemies.append(i)

        if len(available_enemies) == 0:
            available_enemies = MONSTER_NAMES.copy()
            used_monsters.clear()

        new_enemy_name = random.choice(available_enemies)
        used_monsters.append(new_enemy_name)
        new_enemy_pv = int(MONSTER_I_PV*MONSTER_SCALE**difficulty)
        new_weapon_name = random.choice(WEAPON_NAMES)
        new_weapon_power = int(MONSTER_I_POWER*MONSTER_SCALE**difficulty)
        new_weakness = random.choice(list(WEAKNESSES.keys()))

        new_enemy = Monster(new_enemy_name, new_enemy_pv, Weapon(new_weapon_name, new_weapon_power, 0, 0, 0), new_weakness)

        player.max_pv = int(PLAYER_I_PV*PLAYER_SCALE**difficulty)
        player.pv = player.max_pv
        player.max_mana = int(PLAYER_I_MANA*PLAYER_MANA_SCALE**difficulty)
        player.mana = player.max_mana
        player.max_stim = int(PLAYER_I_ULT*PLAYER_ULT_SCALE**difficulty)
        player.can_ult = (player.stim >= player.max_stim)
        fight_result = Fight(player, new_enemy, difficulty, max_analysis, False).fight_loop(max_inv_size, False)

    if isinstance(fight_result, tuple):
        result, overkill = fight_result
    else:
        result = fight_result
        overkill = 0

    if result is True:
        if is_bossfight:
            max_analysis, max_inv_size, max_weapon_slots = offer_upgrades(max_analysis, max_inv_size, max_weapon_slots)

            print("\nTu as battu un haut offier de l'espace mental Roi")
            print("Son arme a l'air forte...")
            wait_input()
            clear_console()
            play_sound("bell")

            b_weapon = gen_boss_weapon(difficulty)

            if len(player.weapons) < max_weapon_slots:
                print(f"""\n Arme "{b_weapon.name}" ajoutée à l'inventaire """)
                player.weapons.append(b_weapon)
                play_sound("bell")
            else:
                def to_display():
                    print("Choisir une arme à jeter :")
                    for j, weapon in enumerate(player.weapons):
                        print(f"[{j+1}] {weapon.name} (Att: {weapon.power}, Ult: {weapon.stim}, Mana: {weapon.mana}, Buffs: {weapon.buff_count})")
                    print(f"[{len(player.weapons)+1}] {b_weapon.name} (Att: {b_weapon.power}, Ult: {b_weapon.stim}, Mana: {b_weapon.mana}, Buffs: 0)")
                def conf(action_input):
                    return action_input.isdigit() and 0 < int(action_input) <= len(player.weapons) +1

                choice = int(solid_input(conf, to_display)) - 1

                if choice < len(player.weapons):
                    print(f"""\n"{player.weapons[choice].name}" jetée""")
                    play_sound("bell")
                    player.weapons[choice] = b_weapon
                else:
                    print(f"\n{b_weapon.name} jetée")
                    play_sound("bell")

            wait_input()

        else:
            if len(player.inventory) >= max_inv_size:
                print("Inventaire plein, pas de loot")
                wait_input()
            else:
                loot = get_rand_obj(player.inventory, difficulty)
                player.inventory.append(loot)
                print(f"""\n L'ennemi a laissé tomber "{loot.name}" (Effet: {loot.effect} {loot.value})""")
                wait_input()

    return fight_result, overkill, max_analysis, max_inv_size, max_weapon_slots

def offer_upgrades(max_analysis, max_inv_size, max_weapon_slots):
    clear_console()
    play_sound("bell")

    def to_display():
        print("\n" + "="*20 + "| AMÉLIORATION |" + "="*20)
        print(f"[1] Capacité d'armes +1 ({max_weapon_slots} -> {max_weapon_slots+1})")
        print(f"[2] Capacité d'objets +1 ({max_inv_size} -> {max_inv_size+1})")
        print(f"[3] Capacité d'analyses +1 ({max_analysis} -> {max_analysis+1})")
    def conf(action_input):
        return action_input.isdigit() and 0 < int(action_input) <= 3

    choice = int(solid_input(conf, to_display))
    if choice == 1:
        print("\nSlot d'arme supplémentaire !")
        wait_input()
        return max_analysis, max_inv_size, max_weapon_slots + 1

    elif choice == 2:
        print("\nSlot d'objet supplémentaire !")
        wait_input()
        return max_analysis, max_inv_size + 1, max_weapon_slots

    elif choice == 3:
        print("\nNombre d'analyses augmenté !")
        wait_input()
        return max_analysis + 1, max_inv_size, max_weapon_slots
    else:
        print("[DEBUG] Erreur dans la fonction conf(action_input)")
        return "gdsofusykgeluqs"
