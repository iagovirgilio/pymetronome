import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from pygame import mixer

class MetronomeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Metronome 1.0')
        self.sound_option_var = tk.IntVar(value=1)

        window_width, window_height = 400, 200
        screen_width = self.winfo_screenwidth()  # Largura da tela do monitor
        screen_height = self.winfo_screenheight()  # Altura da tela do monitor
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        # Definir o diretório de dados dependendo se o aplicativo está congelado ou não
        if getattr(sys, 'frozen', False):
            # O aplicativo está congelado
            datadir = sys._MEIPASS
        else:
            # O aplicativo não está congelado
            datadir = os.path.dirname(__file__)
        
        self.click_sound = os.path.join(datadir, 'click.wav')  # Caminho para o som de clique

        mixer.init()  # Inicializa o módulo mixer
        mixer.music.load(self.click_sound)  # Carrega o som de clique

        self.create_widgets()
        self.bind('<space>', self.spacebar_toggle)
        self.running = False
        self.after_id = None  # Estado do metrônomo
        self.resizable(False, False)

    def create_widgets(self):
        # Configurações dos ticks
        tick_settings_frame = tk.LabelFrame(self, text='Tick Settings...')
        tick_settings_frame.pack(pady=5, padx=10, fill=tk.X)

        # Botão de rádio para som incorporado
        builtin_sound_radio = tk.Radiobutton(
            tick_settings_frame,
            text='Built-in sound',
            variable=self.sound_option_var,
            value=1,
            command=self.on_radio_change
        )

        # Botão de rádio para seleção de arquivo WAV
        wave_file_radio = tk.Radiobutton(
            tick_settings_frame,
            text='Wave File',
            variable=self.sound_option_var,
            value=2,
            command=self.on_radio_change
        )

        builtin_sound_radio.pack(anchor=tk.W)
        wave_file_radio.pack(anchor=tk.W)

        # Configurações de tempo
        tempo_settings_frame = tk.Frame(self)
        tempo_settings_frame.pack(pady=5, padx=10, fill=tk.X)

        self.tempo_label = tk.Label(tempo_settings_frame, text='Tempo (BPM)')
        self.tempo_label.pack()

        # Frame para o controle deslizante e caixa de entrada
        slider_entry_frame = tk.Frame(tempo_settings_frame)
        slider_entry_frame.pack(fill=tk.X, expand=True)

        # Controle deslizante para BPM
        self.tempo_slider = tk.Scale(slider_entry_frame, from_=20, to=240, orient=tk.HORIZONTAL, length=200)
        self.tempo_slider.bind('<ButtonRelease-1>', self.on_slider_release)
        self.tempo_slider.set(120)  # BPM padrão
        self.tempo_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        # Caixa de entrada para digitar BPM
        self.tempo_entry = tk.Entry(slider_entry_frame, bd=5, width=5)
        self.tempo_entry.bind('<KeyRelease>', self.update_slider_from_entry)
        self.tempo_entry.insert(0, '120')  # BPM padrão
        self.tempo_entry.pack(side=tk.LEFT)

        # Botão para iniciar/parar
        start_stop_frame = tk.Frame(tempo_settings_frame)
        start_stop_frame.pack(fill=tk.X)
        self.start_stop_button = tk.Button(start_stop_frame, text='Start/Stop', command=self.toggle_metronome)
        self.start_stop_button.pack(side=tk.TOP, pady=5)

    def on_radio_change(self):
        selected_option = self.sound_option_var.get()
        if selected_option == 1:
            self.on_builtin_sound_selection()
        elif selected_option == 2:
            self.select_wave_file()

    def on_builtin_sound_selection(self):
        self.stop_metronome()  # Parar o metrônomo antes de carregar um novo arquivo de som
        self.click_sound = 'click.wav'  # Define o som de clique padrão
        mixer.music.load(self.click_sound)  # Carrega o som de clique padrão

    def spacebar_toggle(self, event):
        self.toggle_metronome()

    def on_wave_file_radio_change(self):
        if self.wave_file_var.get() == 1:
            self.select_wave_file()

    def on_slider_release(self, event):
        # Update BPM from slider only when the user releases the mouse button
        self.update_bpm_from_slider(self.tempo_slider.get())

    def toggle_metronome(self):
        if self.running:
            self.stop_metronome()
        else:
            self.start_metronome()

    def select_wave_file(self):
        self.stop_metronome()  # Parar o metrônomo antes de carregar um novo arquivo de som
        file_path = filedialog.askopenfilename(
            filetypes=[("Wave Files", "*.wav")], 
            title="Select a .wav file"
        )
        if file_path:
            self.click_sound = file_path
            mixer.music.load(self.click_sound)  # Carrega o arquivo .wav selecionado
            self.sound_option_var.set(2)  # Garantir que o rádio 'Wave File' fique marcado
        else:
            # Se o usuário cancelou, redefinir para o som incorporado
            self.sound_option_var.set(1)  # Isso vai disparar o on_radio_change para 'Built-in sound'

    def start_metronome(self):
        try:
            bpm = int(self.tempo_entry.get())
            if bpm <= 0:
                raise ValueError
            self.running = True
            self.play_click()
        except ValueError:
            messagebox.showerror('Error', 'Please enter a positive integer for BPM.')

    def stop_metronome(self):
        self.running = False
        mixer.music.stop()
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None

    def play_click(self):
        if self.running:
            mixer.music.play()
            # Agora o after_id leva em conta o valor atual do BPM diretamente do slider.
            self.after_id = self.after(int(60 / self.tempo_slider.get() * 1000), self.play_click)

    def update_bpm_from_slider(self, value):
        self.tempo_entry.delete(0, tk.END)
        self.tempo_entry.insert(0, value)
        if self.running:
            # Restart the metronome with new BPM
            self.stop_metronome()
            self.start_metronome()

    def update_slider_from_entry(self, event=None):
        try:
            bpm = int(self.tempo_entry.get())
            if bpm < 20 or bpm > 240:
                # Restringir o valor de BPM para estar dentro dos limites do slider
                raise ValueError
            self.tempo_slider.set(bpm)
            if self.running:
                # Reinicia o metrônomo se o valor de BPM for alterado manualmente
                self.stop_metronome()
                self.start_metronome()
        except ValueError:
            messagebox.showerror('Error', 'Please enter a positive integer for BPM between 20 and 240.')

if __name__ == '__main__':
    app = MetronomeApp()
    app.mainloop()
