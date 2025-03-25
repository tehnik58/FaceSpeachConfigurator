from pydub.playback import play
from PyQt5.QtCore import QThread

class SoundPlayThred(QThread):
    def __init__(self, song, parent = None):
        super(SoundPlayThred, self).__init__(parent)
        self.Song = song

    def run(self):
        play(self.Song)