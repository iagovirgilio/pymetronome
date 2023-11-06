import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from pygame import mixer

# Constantes
DEFAULT_BPM = 120
MIN_BPM = 20
MAX_BPM = 240
WINDOW_WIDTH = 350
WINDOW_HEIGHT = 150
SOUND_FILE = 'click.wav'

class MetronomeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.initialize_window()
        self.initialize_mixer()
        self.create_widgets()
        self.setup_bindings()
        
        self.metronome_running = False
        self.after_id = None

    def initialize_window(self):
        self.title('Metronome 1.0')
        self.set_window_position(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.resizable(False, False)
        self.datadir = self.get_data_directory()
        
    def initialize_mixer(self):
        mixer.init()
        self.click_sound = os.path.join(self.datadir, SOUND_FILE)
        mixer.music.load(self.click_sound)

    def get_data_directory(self):
        if getattr(sys, 'frozen', False):
            return sys._MEIPASS
        return os.path.dirname(__file__)

    def set_window_position(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width/2 - width / 2)
        center_y = int(screen_height/2 - height / 2)
        self.geometry(f'{width}x{height}+{center_x}+{center_y}')

    def create_widgets(self):
        self.create_top_frame()
        self.create_tempo_settings_frame()

    def create_top_frame(self):
        top_frame = tk.Frame(self)
        top_frame.pack(pady=5, padx=10, fill=tk.X)

        tick_settings_frame = self.create_tick_settings_frame(top_frame)
        start_stop_frame = self.create_start_stop_frame(top_frame)

        tick_settings_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        start_stop_frame.pack(side=tk.LEFT, padx=10)

    def create_tick_settings_frame(self, parent):
        frame = tk.LabelFrame(parent, text='Tick Settings')
        self.sound_option_var = tk.IntVar(value=1)

        self.create_radio_button(frame, 'Built-in sound', 1)
        self.create_radio_button(frame, 'Wave File', 2)

        return frame

    def create_radio_button(self, parent, text, value):
        radio_button = tk.Radiobutton(
            parent,
            text=text,
            variable=self.sound_option_var,
            value=value,
            command=self.handle_sound_selection
        )
        radio_button.pack(anchor=tk.W)

    def create_start_stop_frame(self, parent):
        frame = tk.Frame(parent)
        self.start_stop_button = tk.Button(frame, text='Start/Stop', command=self.toggle_metronome)
        self.start_stop_button.pack(side=tk.TOP, pady=5)
        return frame

    def create_tempo_settings_frame(self):
        tempo_settings_frame = tk.Frame(self)
        tempo_settings_frame.pack(pady=5, padx=10, fill=tk.X)

        self.tempo_label = tk.Label(tempo_settings_frame, text='Tempo (BPM)')
        self.tempo_label.pack()

        self.create_slider_entry_frame(tempo_settings_frame)

    def create_slider_entry_frame(self, parent):
        frame = tk.Frame(parent)
        frame.pack(fill=tk.X, expand=True)

        self.tempo_slider = self.create_tempo_slider(frame)
        self.tempo_entry = self.create_tempo_entry(frame)

        self.tempo_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.tempo_entry.pack(side=tk.LEFT)

    def create_tempo_slider(self, parent):
        slider = tk.Scale(parent, from_=MIN_BPM, to=MAX_BPM, orient=tk.HORIZONTAL, length=200)
        slider.bind('<ButtonRelease-1>', self.on_slider_release)
        slider.set(DEFAULT_BPM)
        return slider

    def create_tempo_entry(self, parent):
        entry = tk.Entry(parent, bd=5, width=5)
        entry.bind('<KeyRelease>', self.update_slider_from_entry)
        entry.insert(0, str(DEFAULT_BPM))
        return entry

    def handle_sound_selection(self):
        self.stop_metronome()
        self.load_click_sound()

    def load_click_sound(self):
        if self.sound_option_var.get() == 1:
            self.click_sound = os.path.join(self.datadir, SOUND_FILE)
        else:
            file_path = filedialog.askopenfilename(
                filetypes=[("Wave Files", "*.wav")], 
                title="Select a .wav file"
            )
            self.click_sound = file_path or self.click_sound
        mixer.music.load(self.click_sound)

    def on_slider_release(self, event=None):
        bpm = self.tempo_slider.get()
        self.tempo_entry.delete(0, tk.END)
        self.tempo_entry.insert(0, str(bpm))
        self.update_metronome_tempo(bpm)

    def update_slider_from_entry(self, event=None):
        try:
            bpm = int(self.tempo_entry.get())
            if MIN_BPM <= bpm <= MAX_BPM:
                self.tempo_slider.set(bpm)
                self.update_metronome_tempo(bpm)
            else:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid BPM between 20 and 240.")

    def update_metronome_tempo(self, bpm):
        if self.metronome_running:
            self.stop_metronome()
            self.start_metronome(bpm)

    def setup_bindings(self):
        self.bind('<space>', lambda event: self.toggle_metronome())
        self.bind('<Return>', lambda event: self.toggle_metronome())
        self.bind('<Escape>', lambda event: self.stop_metronome())

    def toggle_metronome(self):
        if self.metronome_running:
            self.stop_metronome()
        else:
            bpm = self.tempo_slider.get()
            self.start_metronome(bpm)

    def start_metronome(self, bpm):
        self.metronome_running = True
        delay = self.bpm_to_ms(bpm)
        self.schedule_tick(delay)

    def stop_metronome(self):
        self.metronome_running = False
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None

    def bpm_to_ms(self, bpm):
        return int((60.0 / bpm) * 1000)

    def schedule_tick(self, delay):
        self.play_click()
        if self.metronome_running:
            self.after_id = self.after(delay, self.schedule_tick, delay)

    def play_click(self):
        mixer.music.play()

if __name__ == "__main__":
    app = MetronomeApp()
    app.mainloop()
