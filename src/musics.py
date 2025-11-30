
import os, random, pygame

from constants import CHANNEL_NUMBER
from settings import sound_enabled


pygame.mixer.init()
pygame.mixer.set_num_channels(CHANNEL_NUMBER)


def play_sound(which, is_bg=False):
    if not sound_enabled():
        return

    variantes = []

    if is_bg:
        if which == "fight":
            directory = [f for f in os.listdir("MUSICS/fight") if f.endswith(".wav")]
            if directory:
                rand_music = random.choice(directory)
                pygame.mixer.music.load(f"MUSICS/fight/{rand_music}")
                pygame.mixer.music.play(loops=-1)
                pygame.mixer.music.set_volume(0.15)
        elif which == "boss":
            pygame.mixer.music.load(f"MUSICS/fight/boss.mp3")
            pygame.mixer.music.play(loops=-1)
            pygame.mixer.music.set_volume(0.2)
        else:
            pygame.mixer.music.load(f"MUSICS/{which}.mp3")
            pygame.mixer.music.play(loops=-1)
            pygame.mixer.music.set_volume(0.15)
    else:
        for _ in os.listdir("SFX"):
            if _.startswith(which) and _.endswith(".mp3"):
                variantes.append(_)
        sound = random.choice(variantes)

        f_sound = pygame.mixer.Sound(f"SFX/{sound}")
        pygame.mixer.find_channel(True).play(f_sound)

def stop_sound(ms):
    pygame.mixer.music.fadeout(ms)