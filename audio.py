# audio.py
"""
Gestione effetti sonori e musica di sottofondo.
"""
import pygame
import os

class AudioManager:
    def __init__(self, config):
        self.config = config
        pygame.mixer.init()
        base = os.path.join(os.path.dirname(__file__), "assets")
        self.sounds = {
            "claim": self._load_sound(base, "claim.wav"),
            "link": self._load_sound(base, "link.wav"),
            "error": self._load_sound(base, "error.wav"),
            "success": self._load_sound(base, "success.wav")
        }
        self.music_on = True
        self.music_file = os.path.join(base, "music.ogg")
        self.music_volume = 0.5
        self.sfx_volume = 0.7
        self._play_music()

    def _load_sound(self, base, name):
        try:
            return pygame.mixer.Sound(os.path.join(base, name))
        except Exception:
            return None

    def play(self, name):
        if self.sounds.get(name):
            self.sounds[name].set_volume(self.sfx_volume)
            self.sounds[name].play()

    def _play_music(self):
        if self.music_on and os.path.exists(self.music_file):
            pygame.mixer.music.load(self.music_file)
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(-1)

    def toggle_music(self):
        self.music_on = not self.music_on
        if self.music_on:
            self._play_music()
        else:
            pygame.mixer.music.stop()

    def set_music_volume(self, vol):
        self.music_volume = vol
        pygame.mixer.music.set_volume(vol)

    def set_sfx_volume(self, vol):
        self.sfx_volume = vol
