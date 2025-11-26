
import json

with open("JSON/cst_data.json", "r", encoding="utf-8") as read_file:
    _CST_DATA = json.load(read_file)

MONSTER_NAMES = _CST_DATA.get("monster_names", [])
BOSS_NAMES = _CST_DATA.get("boss_names", [])
WEAPON_NAMES = _CST_DATA.get("weapon_names", [])
OBJECT_BLUEPRINTS = _CST_DATA.get("object_blueprints", [])
RANDOM_LINES = _CST_DATA.get("rand_lines", [])
WEAKNESSES = _CST_DATA.get("weaknesses", {})

_GAME_CONSTANTS = _CST_DATA.get("game_constants", {})

ULT_COEFFICIENT = _GAME_CONSTANTS.get("ult_coefficient", 4)
MAX_INV_SIZE = _GAME_CONSTANTS.get("max_inv_size", 6)
OBJECT_SCALE = _GAME_CONSTANTS.get("object_scale", 1.05)
OBJECT_SCALE_SLOWDOWN = _GAME_CONSTANTS.get("object_scale_slowdown", 4)
SHIELD_NERF = _GAME_CONSTANTS.get("shield_nerf", 0.7)
MAX_NAV_ITERATIONS = _GAME_CONSTANTS.get("max_nav_iterations", 30)
FADE_OUT = _GAME_CONSTANTS.get("fade_out", 2500)
MISS_CHANCE = _GAME_CONSTANTS.get("miss_chance", 0.05)
HEAL_CHANCE = _GAME_CONSTANTS.get("heal_chance", 0.05)
HEAL_AMOUNT = _GAME_CONSTANTS.get("heal_amount", 0.1)
MAX_ANALYSIS = _GAME_CONSTANTS.get("max_analysis", 1)
MAX_WEAPON_SLOTS = _GAME_CONSTANTS.get("max_weapon_slots", 3)
OVERKILL_MULT = _GAME_CONSTANTS.get("overkill_score_multiplier", 2)
CHEAT_CODE = _GAME_CONSTANTS.get("cheat_code", "zahoe")

# PLAYER SCALING
PLAYER_I_PV = _GAME_CONSTANTS.get("player_i_pv", 100)
PLAYER_I_MANA = _GAME_CONSTANTS.get("player_i_mana", 10)
PLAYER_I_ULT = _GAME_CONSTANTS.get("player_i_ult", 200)
PLAYER_SCALE = _GAME_CONSTANTS.get("player_scale", 1.16)
PLAYER_ULT_SCALE = _GAME_CONSTANTS.get("player_ult_scale", 1.05)

# MONSTERS SCALING
MONSTER_I_PV = _GAME_CONSTANTS.get("monster_i_pv", 200)
MONSTER_I_POWER = _GAME_CONSTANTS.get("monster_i_power", 10)
MONSTER_SCALE = _GAME_CONSTANTS.get("monster_scale", 1.18)

BOSS_I_PV = _GAME_CONSTANTS.get("boss_i_pv", 200)
BOSS_I_POWER = _GAME_CONSTANTS.get("boss_i_power", 15)
BOSS_SCALE = _GAME_CONSTANTS.get("boss_scale", 1.20)

# WEAPONS
CLASSIC_N = _GAME_CONSTANTS.get("classic_n", 10)
OP_N = _GAME_CONSTANTS.get("op_n", 11)
NUM_CLASSIC_STARTER = _GAME_CONSTANTS.get("num_classic_starter", 4)
NUM_OP_STARTER = _GAME_CONSTANTS.get("num_op_starter", 1)
WEAPON_MIN_MANA = _GAME_CONSTANTS.get("weapon_min_mana", 3)
WEAPON_MAX_MANA = _GAME_CONSTANTS.get("weapon_max_mana", 5)
NAME_MIN_LETTER = _GAME_CONSTANTS.get("name_min_letter", 4)
NAME_MAX_LETTER = _GAME_CONSTANTS.get("name_max_letter", 7)
GEN_ATTEMPTS = _GAME_CONSTANTS.get("gen_attempts", 111)
