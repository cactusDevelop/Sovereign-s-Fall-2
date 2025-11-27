"""
                                                      .::.       ^7
                                                  .^7JPB#&@#GJ^  .7&@BJ?JYYJ7~:
                                              .~YG#@@@@@@@@@@@@BG#@@@@@@@@@@@@&G7
                                            ^Y#@@@@@@@@@@@@@@@@@@@@@@@@G@@@@@@@@@G.
                                          Y#@@@@@@@@@@@@@@@@@@@@@@@@@@YG@@@&5&@@@@!
                                          5@@@@@@@@@@@@@@@@@@@@@@@@@@JY@@&Y7G@@@@@^
                                          :&@@@@@@@@@@@@@@@@@@@@@@@@??@@#JP@@#&@@?
                                          :G@@@@@@@@@@@@@@@#BB#@@@Y:7@@@@@&P5#@@J
                                            7B@@@@@@@@@@@@G..J&@@G.Y@@@@@GG&@#@B
                                             .?&@@@@@@@@@@J  ^#@@5B@@@@@@@@#!^G5
                                               :P@@@@@@@@&:  ~&@B#@@@@@@@@5.~G@?
                                        :~!7~    ?@@@@@@@@~ .#@@@@@@@@@@P^ J@@Y   .!7??JYPGBBBBP5?^
                                      :7JJJJJ?.   ~&@@@@@@7 5@@@@@@@@@&7  5@B!  :JG?^P@@@@@@@&&@@@@B?.
                    :~!7!~.          ^JJJ?JJJJ?!~: ~&@@@@@!7@@@@@@@@@G: 7GP! .7GB?:.Y#@@@&BPPG&@@@@@@^
                  :7JJJJJJJ!.       :JJJJ!JJ7JJJJ?77P@@@@@7#@@@@@@@@J 7B@BJJG@@5. ^P@#Y!7YG&@@@@@@@@J
                 ^JJJJJ??JJJ?^     :?JJJ?~J?~JJJJJJJJB@@@#P@@@@@@@B~~G@@@@@@@B!:JB&&B55B&@#PYYP&@@@?
               ~?JJJJJJ?^?J7JJ?!:  ~7^?Y!^J?J?7JJJJJJ5@@@&@@@@@@@Y!P@@@@@@@#YJG@@@@&@@@@@@&##&@@@@G
               .?JJJ?!?J77J!J?:7J~ .?.:??!JJJ7J?JJJJJJ#@@@@@@@@BJP@@@@@@@&BG#@@@@@@@@@@&BGPG&@@@@@&7
            .^~7JJJJJJ!!JJJ??J!.7Y^ ?7 ~JJJJJJ?.!JJJJJB@@@@@@&PP&@@@@@@@@&@@@@@@@@@@@@@@@@@@@@@@@@Y:
           ^?JJJJJJJJJJ!:?JJJJJ^ 77:?J~^JJJJJJ^.?JJJJJG@@@@@#G#@@@@@@@@@@@@@@@@@@&#P5Y7!7#@@@@@@@@@B!.
           ?JJJJJJJJJJJJ!~?JJJJJ: 7JJJJ~?JJJJ? ^JJJJJJB@@@&##@@@@@@@@@@@@@@&#GY?~:.:!J5G#@@@@@@@@@@@&7
          ^JJJJJJJJJJJ!7JJ?JJJJJJ:^JJJJ??JJJJ~:?JJJJ?!B@@@@@@@@@@@@@&&#BG5YJ??J55GB&@@@@@@@@@@@@@@@#:
          !JJJJJJJJJJ?:..:7JJJJJJJ:!JJJJJJJJ?:?YJ7~: :&@@@@@@@@@@@&###&&@@@@@@@@@@@@@@@@@@@@@@@@@@@7
          !JJJJJJJJJJJJ?^..^?JJJJJ?^?JJJJJJJ!7J!:    Y@@@@#GY7~^^:::^~!7JPB&@@@@@@@@@@@@@@@@@@@@@@B.
          ^JJJJJJJJJJJJJJJ?!~!?JJJJ?!JJJJJJJ7!.     ~@@#Y~.                .^7YB&@@@@@@@@@@@@@@@@Y.
          :7??JJJJJJJ???JJJJJ???JJJJ77JJJJJ7:      ^&#?^:^^:^^^^^^^:...         :!YB@@@@@@@@@@@@@#.
             .^^^:........::^~77JJJJJ??JJJ?.      ~#Y:~~!!!!!!!!!!~~~~~~~~~~~~.     ^?5GB&@@@@YJ5?
                                .^!?JJJJJJ^      7B~  ~~~~~~~^^^~~~~!^^~~~~!~^.          :~!!:
                                    :!?JJJ:    .YG:   :!~~^:^^~~~~~~^^^^^~~:.
                                      .~?Y^   ~G?     ^~~~~~!~~~~~~^^:::::............
                                        .!? .YG^   .:~~~~~~~~~~~~^^^::^^^^~~~~~~~~~~~~~.
                                          ^JGY..:^^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~!!!^.
                             ........... ^PG?. .........::^^~~~~~^^^:::^^~~~~~~~~~~^::.
                                        J&5.:!                .:^~~~~~~~~~~~~~~~!!!:
                                       P&!   ^!                   .:^~!!!!!!!!~~^:.
                                       7:     ~!                     .::^^^::..
                                               !!
                                                7!
                                                 :.
"""

import pygame, random

from json_manager import *
from global_func import *
from musics import play_sound, stop_sound
from online_highscores import get_online_highscore, get_online_leaderboard
from scenes import launch_cutscene, launch_starters_scene, launch_tuto_fight, game_over
from constants import _HS, OVERKILL_MULT, MAX_ANALYSIS, MAX_INV_SIZE, MAX_WEAPON_SLOTS, CHEAT_CODE, CHEAT_COLOR, GOLD, SILVER, BRONZE, BOLD, REV_YELLOW, RESET


# CACHER LES MESSAGES D'ERREUR IN FINE
"""import sys

class DevNull:
    def write(self, msg):
        pass

sys.stderr = DevNull()"""


def add_score(points:int):
    data["player"]["score"] += points

# MENU
def display_menu():
    def to_display_m():
        if not pygame.mixer.music.get_busy():
            play_sound("menu", True)
        print("\n" + "="*5 + f"| {BOLD}MAIN MENU{RESET} |" + "="*(get_width()-18))

        if data.get("cheat", False):
            print(f"\n{CHEAT_COLOR} >>> MODE CHEAT ACTIF <<< {RESET}")
            print("*Nouvelle partie sans cheat*")

        try:   # [BALISE ONLINE HIGHSCORES]
            online_hs = get_online_highscore()
            if online_hs > 0:
                line_2 = f"░█{REV_YELLOW} RECORD MONDIAL : {online_hs} {RESET}░█"

                print("\n ░█"+"█"*(len(line_2)-15))
                print(line_2)
                print(" ░█" + "█"*(len(line_2)-15))
        except:
            if _HS["highscore"] > 0:
                print("\n " + "_" * 10)
                print(f"| TOP LOCAL : {_HS['highscore']}")
                print("|" + "_" * 20)


        print("\n [1] Nouvelle Partie")
        print(f" [2] Charger Une Partie")
        print(" [3] Classement")
        print(" [4] Seeded run")
        print(" [0] Quitter :‹")

    def conf_m(action_input):
        return action_input.lower() in ["0", "1", "2", "3", "4", CHEAT_CODE]

    clear_console()
    direc = solid_input(conf_m, to_display_m)

    if direc == CHEAT_CODE:
        print(f"\n{CHEAT_COLOR} >>> CHEAT MODE ACTIF <<< {RESET}")
        play_sound("win")
        time.sleep(2.5)
        data["cheat"] = True

        with open("JSON/active_data.json", "w", encoding="utf-8") as write_cheat:
            json.dump(data, write_cheat, indent=4, ensure_ascii=False)

        return 1

    return int(direc)


def show_hs():  # [BALISE ONLINE HIGHSCORES]
    print("\n" + "=" * 5 + f"| {BOLD}ALL TIME TOP 10{RESET} |" + "=" * (get_width() - 24))

    try:
        online_scores = get_online_leaderboard()
        if online_scores is None:  # Changez ici : testez explicitement None
            print("Aucun score en ligne...")
        elif len(online_scores) == 0:  # Ajoutez ce test pour liste vide
            print("Aucun score enregistré pour le moment...")
        else:
            for rank, entry in enumerate(online_scores, 1):
                date = entry.get('date', '')[:10] if 'date' in entry else ''

                if rank == 1:
                    color = GOLD
                    medal = "🥇"
                elif rank == 2:
                    color = SILVER
                    medal = "🥈"
                elif rank == 3:
                    color = BRONZE
                    medal = "🥉"
                else:
                    color = ""
                    medal = "  "

                nickname_display = f"{entry['nickname']}"
                score_info = f"{entry['score']} pts (niveau {entry['level']})"
                date_display = f" [{date}]" if date else ""

                print(f"{medal} {rank:2}) {color}{nickname_display:<20}{RESET} - {score_info}{date_display}")
    except:
        print("Impossible de récupérer les scores en ligne")
        print("\n--- SCORES LOCAUX ---")
        if not _HS["history"]:
            print("Aucun score local...")
        else:
            for rank, entry in enumerate(_HS["history"], 1):
                nickname = str(entry['nickname'])[:20]
                score_info = f"{entry['score']} pts (niveau {entry['level']})"
                print(f"   {rank:2}) {nickname:<20} - {score_info}")

    input("\nRetour >")


# CUTSCENE
def run_intro():
    is_cheating = data.get("cheat", False)

    if data.get("seed") is None:
        data["seed"] = int((random.getstate()[1][0]*time.time())%67676767)
        random.seed(data["seed"])

    data["player"]["score"] = 0
    data["player"]["current_level"] = 0
    data["player"]["weapons_inv"] = {}
    data["player"]["objects_inv"] = {}
    data["used_monsters"] = []
    data["cheat"] = is_cheating

    if not launch_cutscene(data):
        game_over(data,1,"Tié mort vite")
        return None

    launch_starters_scene(data)

    player = get_player_data()
    save_game(player, 0, data["used_monsters"])

    tuto_result = launch_tuto_fight(player)

    if not tuto_result:
        game_over(data, 3, "T'abuses...")
        return None
    elif tuto_result == "gameover2":
        game_over(data, 2, "Tu n'es pas la chips la plus croustillante toi")
        return None

    add_score(100)
    data["player"]["current_level"] = 1
    save_game(player, 1, data["used_monsters"])
    run_fight_loop()
    return None


def run_fight_loop():
    from scenes import launch_keep_fighting, game_over

    fighting = True

    current_max_analysis = MAX_ANALYSIS
    current_max_inv_size = MAX_INV_SIZE
    current_max_weapon_slots = MAX_WEAPON_SLOTS

    while fighting:
        player = get_player_data()
        lvl = data["player"]["current_level"]
        u_m = get_used_monsters()

        fight_result, overkill, current_max_analysis, current_max_inv_size, current_max_weapon_slots = launch_keep_fighting(
            lvl, player, u_m, current_max_analysis, current_max_inv_size, current_max_weapon_slots)

        if fight_result:
            add_score(20 * lvl)
            if overkill > 0:
                add_score(int(overkill*OVERKILL_MULT))

            lvl += 1
            data["player"]["current_level"] = lvl
            save_game(player, lvl, u_m)
        else:
            fighting = False
            game_over(data, 4, "Parti si tôt...")


# GAME LOOP
if __name__ == "__main__":
    running = True
    save_size()

    while running:
        menu_to = display_menu()

        if menu_to == 0:
            print("\nTu reviendras quand tu seras prêt")
            stop_sound(1500)
            time.sleep(1.7)
            running = False
        if menu_to == 1:
            data["cheat"] = False
            data["seed"] = None
            with open("JSON/active_data.json", "w", encoding="utf-8") as write_file:
                json.dump(data, write_file, indent=4, ensure_ascii=False)
            run_intro()
        elif menu_to == 2:
            if not saved_game():
                input("\nAucune partie sauvegardée... ¯\_(ツ)_/¯")
                continue
            print(f"\nPartie Trouvée: ({get_save()['nickname']} - Niveau {get_save()['level']})")
            print("Let's go ! > ", end="")
            wait_input()
            run_fight_loop()
        elif menu_to == 3:
            clear_console()
            print()
            show_hs()
        elif menu_to == 4:
            clear_console()
            def to_display():
                print("\n" + "=" * 5 + f"| {BOLD}DEV MODE{RESET} |" + "=" * (get_width() - 17))
                print("\nVeuillez entrer la seed désirée (0 pour retour)")
            def conf(x):
                return x.isdigit() or (x.startswith("-") and x[1:].isdigit())

            seed = int(solid_input(conf, to_display))

            if seed != 0:
                random.seed(seed)
                data["seed"] = seed
                print(f"[SEEDED RUN] /{seed}/")
                time.sleep(2)

                import scenes
                scenes.starters = None

                run_intro()
            else:
                continue
                