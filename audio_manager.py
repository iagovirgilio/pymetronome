import os
from pygame import mixer
from constants import SOUND_FILE

class AudioManager:
    def __init__(self, data_directory):
        self.data_directory = data_directory
        self.initialize_mixer()

    def initialize_mixer(self):
        mixer.init()
        self.click_sound = os.path.join(self.data_directory, SOUND_FILE)
        mixer.music.load(self.click_sound)

    def load_click_sound(self, sound_option, custom_path=''):
        if sound_option == 1:
            self.click_sound = os.path.join(self.data_directory, SOUND_FILE)
        else:
            self.click_sound = custom_path
        mixer.music.load(self.click_sound)

    def play_click(self):
        mixer.music.play()
