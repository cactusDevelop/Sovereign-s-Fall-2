
import requests
from datetime import datetime

FIREBASE_URL = "https://sovereign-s-fall-2-default-rtdb.europe-west1.firebasedatabase.app"
SCORES_PATH = "/highscores.json"

ADMIN_TOKEN = "W2xCkZiTIQSqJ4s97Gv4eGPF4J1qmzEWhhoqQkZE"


class FirebaseScores:
    def __init__(self):
        self.enabled = True

        if not self.enabled:
            print("[INFO] Firebase non configuré - Mode local uniquement")

    def _get_url(self, with_auth=False):
        url = f"{FIREBASE_URL}{SCORES_PATH}"
        if with_auth:
            url += f"?auth={ADMIN_TOKEN}"
        return url

    def fetch_online_scores(self):
        if not self.enabled:
            return None

        try:
            response = requests.get(self._get_url(with_auth=False), timeout=5)

            if response.status_code == 200:
                data = response.json()

                if data is None:
                    return self._initialize_database()

                return data

            return None

        except requests.exceptions.Timeout:
            print("[ERREUR] Timeout - Vérifie ta connexion")
            return None
        except Exception as e:
            print(f"[ERREUR] Fetch failed: {e}")
            return None

    def _initialize_database(self):
        initial_data = {
            "highscore": 0,
            "history": []
        }

        try:
            # Écriture avec authentification
            response = requests.put(
                self._get_url(with_auth=True),
                json=initial_data,
                timeout=5
            )

            if response.status_code == 200:
                print("[INFO] Firebase initialisé avec succès")
                return initial_data

        except Exception as e:
            print(f"[ERREUR] Initialisation échouée: {e}")

        return None

    def _validate_score(self, nickname, score, level):
        if score < 0 or level < 0:
            return False
        if score > 999999999 or level > 10000:
            return False
        if not nickname or len(nickname) > 50:
            return False

        from constants import SCORE_MULT, OVERKILL_MULT
        max_theoretical = (SCORE_MULT * level * 3) + (level * 1000 * OVERKILL_MULT)

        if score > max_theoretical:
            print(f"[ANTI-TRICHE] Score suspect rejeté : {score} pts au niveau {level}")
            return False

        return True

    def push_score(self, nickname, score, level):
        if not self.enabled:
            return False

        if not self._validate_score(nickname, score, level):
            print("[ERREUR] Score invalide")
            return False

        try:
            current_data = self.fetch_online_scores()

            if current_data is None:
                print("[ERREUR] Impossible de synchroniser")
                return False

            new_entry = {
                "nickname": str(nickname)[:50],
                "score": int(score),
                "level": int(level),
                "date": datetime.now().isoformat()
            }

            current_data["history"].append(new_entry)

            current_data["history"] = sorted(
                current_data["history"],
                key=lambda x: x["score"],
                reverse=True
            )[:10]

            if score > current_data.get("highscore", 0):
                current_data["highscore"] = int(score)

            response = requests.put(
                self._get_url(with_auth=True),
                json=current_data,
                timeout=5
            )

            if response.status_code == 200:
                print(f"✓ Score envoyé en ligne : {score} pts")
                return True
            else:
                print(f"[ERREUR] Envoi échoué: {response.status_code}")
                return False

        except Exception as e:
            print(f"[ERREUR] Push failed: {e}")
            return False

    def get_top_10(self):
        if not self.enabled:
            return None

        data = self.fetch_online_scores()
        if data:
            return data.get("history", [])
        return None

    def get_highscore(self):
        if not self.enabled:
            return None

        data = self.fetch_online_scores()
        if data:
            return data.get("highscore", 0)
        return None


def save_online_score(nickname, score, level):
    firebase = FirebaseScores()
    return firebase.push_score(nickname, score, level)


def get_online_leaderboard():
    firebase = FirebaseScores()
    return firebase.get_top_10()


def get_online_highscore():
    firebase = FirebaseScores()
    return firebase.get_highscore()


def save_score_with_fallback(nickname, score, level, local_save_func):

    online_success = False

    try:
        if save_online_score(nickname, score, level):
            online_success = True
    except:
        pass

    local_highscore = local_save_func(nickname, score, level)

    if not online_success:
        print("⚠ Sauvegarde locale uniquement")

    return local_highscore