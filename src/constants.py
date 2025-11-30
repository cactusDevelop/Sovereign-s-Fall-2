
import json

with open("JSON/cst_data.json", "r", encoding="utf-8") as read_file:
    _CST_DATA = json.load(read_file)
with open("JSON/highscores.json", "r", encoding="utf-8") as read_hs:
    _HS = json.load(read_hs)

MONSTER_NAMES = _CST_DATA.get("monster_names", [])
BOSS_NAMES = _CST_DATA.get("boss_names", [])
WEAPON_NAMES = _CST_DATA.get("weapon_names", [])
OBJECT_BLUEPRINTS = _CST_DATA.get("object_blueprints", [])
RANDOM_LINES = _CST_DATA.get("rand_lines", [])
WEAKNESSES = _CST_DATA.get("weaknesses", {})
_GAME_CONSTANTS = _CST_DATA.get("game_cst", {})

for key, value in _GAME_CONSTANTS.items():
    globals()[key.upper()] = value

# PYTHON CST
INCOGNITO = " \033[1;32m???\033[0m"
ALPHABET = 'a' * 82 + 'b' * 10 + 'c' * 32 + 'd' * 37 + 'e' * 150 + 'f' * 11 + 'g' * 10 + 'h' * 9 + 'i' * 73 + 'j' * 5 + 'k' * 30 + 'l' * 57 + 'm' * 29 + 'n' * 40 + 'o' * 53 + 'p' * 28 + 'q' * 12 + 'r' * 66 + 's' * 81 + 't' * 50 + 'u' * 64 + 'v' * 16 + 'w' * 0 + 'x' * 4 + 'y' * 80 + 'z' * 2

# ANSI
RED = "\033[1;31m"
GREEN = "\033[1;32m"
CYAN = "\033[1;36m"
GREY = "\033[90m"
BLUE = "\033[1;94m"
GOLD = "\033[1;93m"
SILVER = "\033[1;38m"
BRONZE = "\033[1;38;5;208m"

CHEAT_COLOR = "\033[42m"
REV_YELLOW = "\033[33;7m"
REV_WHITE = "\033[0;7m"
REV_B_W = "\033[1;7m"

BOLD = "\033[1m"
RESET = "\033[0m"

TITLE: str
GAME_TITLE: str
SCORE_MULT: int
ULT_COEFFICIENT: int
MAX_INV_SIZE: int
OBJECT_SCALE: float
OBJECT_SCALE_SLOWDOWN: int
SHIELD_NERF: float
MAX_NAV_ITERATIONS: int
FADE_OUT: int
MISS_CHANCE: float
HEAL_CHANCE: float
HEAL_AMOUNT: float
MAX_ANALYSIS: int
MAX_WEAPON_SLOTS: int
PLAYER_I_PV: int
PLAYER_I_MANA: int
PLAYER_I_ULT: int
PLAYER_SCALE: float
PLAYER_ULT_SCALE: float
PLAYER_MANA_SCALE: float
SHIELD_SCALE: float
MONSTER_I_PV: int
MONSTER_I_POWER: int
MONSTER_SCALE: float
BOSS_I_PV: int
BOSS_I_POWER: int
BOSS_SCALE: float
BASE_WEAPON: int
OP_BONUS: int
NUM_CLASSIC_STARTER: int
NUM_OP_STARTER: int
WEAPON_MIN_MANA: int
WEAPON_MAX_MANA: int
WEAPON_MANA_SCALE: float
NAME_MIN_LETTER: int
NAME_MAX_LETTER: int
GEN_ATTEMPTS: int
OVERKILL_MULT: int
CHANNEL_NUMBER: int
CHEAT_CODE: str