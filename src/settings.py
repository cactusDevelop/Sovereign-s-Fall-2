
import json, os


DEFAULT_SETTINGS = {
    "animations_enabled": True,
    "sound_enabled": True,
    "typew_speed": 0.1
}

def load_settings():
    if not os.path.exists("JSON/settings.json"):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    try:
        with open("JSON/settings.json", "r", encoding="utf-8") as f:
            settings = json.load(f)
            for key in DEFAULT_SETTINGS:
                if key not in settings:
                    settings[key] = DEFAULT_SETTINGS[key]
            return settings
    except:
        return DEFAULT_SETTINGS.copy()

_current_settings = load_settings()

def save_settings(settings):
    try:
        os.makedirs("JSON", exist_ok=True)
        with open("JSON/settings.json", "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"[DEBUG] Impossible de sauvegarder les paramètres: {e}")
        return False

def get_setting(key):
    settings = load_settings()
    return settings.get(key, DEFAULT_SETTINGS.get(key))

def set_setting(key, value):
    settings = load_settings()
    settings[key] = value
    save_settings(settings)

def animations_enabled():
    return _current_settings.get("animations_enabled", True)

def sound_enabled():
    return _current_settings.get("sound_enabled", True)

def get_typew_speed():
    return _current_settings.get("typew_speed", 0.1)

def refresh_settings():
    global _current_settings
    _current_settings = load_settings()