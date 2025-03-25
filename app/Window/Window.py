from PyQt5.QtWidgets import QMainWindow, QFileDialog, QListView, QListWidgetItem
import pyqtgraph as pg
from PyQt5 import uic, QtCore

import speech_recognition as sr
from pydub import AudioSegment
from dataclasses import dataclass

from Handler.SoundHandler import SoundPlayThred

class MyWindowClass(QMainWindow, uic.loadUiType("source/MainScreen.ui")[0]):
    AudioFile:  str
    Song:       AudioSegment
    Max_height_song: int
    plots: dict = {}
    length: float
    wordsList = {}
    actualWord = ''
    actualIndexChar: int

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        
        self.plot_graph = pg.PlotWidget(self)
        self.horizontalBase.addWidget(self.plot_graph)
        self.plot_graph.setFixedSize(QMainWindow.width(self)-100, QMainWindow.height(self) - 100)
        self.pen = pg.mkPen(color=(255, 0, 0), width=2, style=QtCore.Qt.DashLine)
        self.pen1 = pg.mkPen(color=(0, 255, 0), width=2, style=QtCore.Qt.DashLine)

    def playButtonClicked(self):
        self.SoundHandlerThred_instance = SoundPlayThred(self.Song)
        self.SoundHandlerThred_instance.start()

    def SetButtonClick(self):
        self.wordsList[self.actualWord][self.actualIndexChar] = self.doubleSpinBox.value()
        if not self.actualWord in self.plots.keys():
            self.plots[self.actualWord] = {}
            for i,u in enumerate(self.actualWord):
                if i != self.actualIndexChar:
                    self.plots[self.actualWord][f'{i}'] = self.plot_graph.plot([0, 
                                                                                0],
                                                                           [-self.Max_height_song, 
                                                                            self.Max_height_song])
        else:
            self.plot_graph.removeItem(self.plots[self.actualWord][f'{self.actualIndexChar}'])
        self.plots[self.actualWord][f'{self.actualIndexChar}'] = self.plot_graph.plot([self.wordsList[self.actualWord][self.actualIndexChar], 
                                                                    self.wordsList[self.actualWord][self.actualIndexChar]],
                                                                   [-self.Max_height_song, 
                                                                    self.Max_height_song], 
                                                                    pen = self.pen1)

    def onWordClick(self, item:QListWidgetItem):
        self.listWidget_2.clear()
        self.actualWord = item.text()
        for i in item.text():
            self.listWidget_2.addItem(QListWidgetItem(i))

    def onCharClick(self, item:QListWidgetItem):
        print(self.actualWord)
        print(self.wordsList[self.actualWord])
        self.doubleSpinBox.setValue(self.wordsList[self.actualWord][list(self.actualWord).index(item.text())])
        self.actualIndexChar = list(self.actualWord).index(item.text())

    def fileButtonClicked(self):
        self.plot_graph.plotItem.clear()
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*)", options=options)
        if fileName:
            self.listWidget_2.clear()
            self.listWidget.clear()
            self.FileLable.setText(fileName)
            self.Song = AudioSegment.from_mp3(fileName)

            sound = AudioSegment.from_mp3(fileName)
            fileName1 = fileName.replace(".mp3",".wav")
            print(fileName1)
            sound.export(fileName1, format="wav")
            file_audio = sr.AudioFile(fileName1)                                       
            r = sr.Recognizer()

            with file_audio as source:
                audio_text = r.record(source)
                text = str(r.recognize_google(audio_text, language="ru-RU"))
                print(text)
                self.AudioFile = fileName
                self.Song = AudioSegment.from_file(fileName)

                self.Max_height_song = max(self.Song.get_array_of_samples())

                print(f'Max_height_song: {self.Max_height_song}')
                count = len(self.Song.get_array_of_samples())
                l = []
                length = []
                for i, s in enumerate(self.Song.get_array_of_samples()):
                    if i % 10 == 0:
                        length.append(i/count*(count/self.Song.frame_rate))
                        l.append(s)

                self.length = count/self.Song.frame_rate
                self.plots['audio'] = self.plot_graph.plot(length, l)
                self.plots['linePlayStart'] = self.plot_graph.plot([0, 0],[-self.Max_height_song, self.Max_height_song], pen = self.pen)
                self.plots['linePlayEnd'] = self.plot_graph.plot([self.length, self.length],[-self.Max_height_song, self.Max_height_song], pen = self.pen)
                
                for x in text.split(' '):
                    self.listWidget.addItem(QListWidgetItem(x))
                    self.wordsList[x] = [0. for ch in x]
                    print(self.wordsList, self.wordsList[x])

                self.plots: dict = {}
                self.actualWord = ''
                self.actualIndexChar: int