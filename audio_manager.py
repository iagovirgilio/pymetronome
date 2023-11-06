from pygame import mixer
import os
from constants import SOUND_FILE

class AudioManager:
    def __init__(self, data_directory):
        self.data_directory = data_directory
        mixer.init()
        self.click_sound = os.path.join(self.data_directory, SOUND_FILE)
        mixer.music.load(self.click_sound)

    def play_click(self):
        mixer.music.play()

    def load_click_sound(self, sound_option, custom_sound=None):
        if sound_option == 1:
            self.click_sound = os.path.join(self.data_directory, SOUND_FILE)
        elif sound_option == 2 and custom_sound:
            self.click_sound = custom_sound
        mixer.music.load(self.click_sound)
