
import os, random, pygame

from constants import CHANNEL_NUMBER, BG_VOLUME, SFX_VOLUME
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
                pygame.mixer.music.set_volume(BG_VOLUME)
        elif which == "boss":
            pygame.mixer.music.load(f"MUSICS/fight/boss.mp3")
            pygame.mixer.music.play(loops=-1)
            pygame.mixer.music.set_volume(BG_VOLUME)
        else:
            pygame.mixer.music.load(f"MUSICS/{which}.mp3")
            pygame.mixer.music.play(loops=-1)
            pygame.mixer.music.set_volume(BG_VOLUME)
    else:
        for _ in os.listdir("SFX"):
            if _.startswith(which) and _.endswith(".mp3"):
                variantes.append(_)
        sound = random.choice(variantes)

        f_sound = pygame.mixer.Sound(f"SFX/{sound}")
        f_sound.set_volume(SFX_VOLUME)
        pygame.mixer.find_channel(True).play(f_sound)

def stop_sound(ms):
    pygame.mixer.music.fadeout(ms)