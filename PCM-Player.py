import tkinter as tk
from tkinter import filedialog
from pydub import AudioSegment
from pydub.playback import play
import threading

class PCMPlayer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PCM Player")

        self.play_rate_label = tk.Label(self.root, text="Play Rate (Hz):")
        self.play_rate_label.grid(row=0, column=0, padx=5, pady=5)

        self.play_rate_entry = tk.Entry(self.root)
        self.play_rate_entry.grid(row=0, column=1, padx=5, pady=5)
        self.play_rate_entry.insert(0, "8192")

        self.select_button = tk.Button(self.root, text="Select PCM file", command=self.select_pcm_file)
        self.select_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        self.play_button = tk.Button(self.root, text="Play", command=self.play_pcm)
        self.play_button.grid(row=2, column=0, padx=5, pady=5)

        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_pcm)
        self.stop_button.grid(row=2, column=1, padx=5, pady=5)

        self.file_path = ""

    def select_pcm_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("PCM files", "*.pcm")])

    def play_pcm(self):
        if self.file_path:
            play_rate = int(self.play_rate_entry.get()) if self.play_rate_entry.get() else 8192
            threading.Thread(target=self._play_audio, args=(self.file_path, play_rate)).start()

    def stop_pcm(self):
        play.stop()

    def _play_audio(self, file_path, play_rate):
        chunk = 1024

        sound = AudioSegment.from_file(file_path, format="pcm", frame_rate=play_rate, channels=2, sample_width=2)

        play(sound)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    player = PCMPlayer()
    player.run()
