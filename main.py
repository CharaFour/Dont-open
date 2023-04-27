from tkinter import *
from tkinter import filedialog as fd
import os
import vlc
import random

Instance = vlc.Instance()
player = Instance.media_player_new()

class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, background="#EEEEEE")   
        self.parent = parent
        self.initUI()
        self.centerWindow()
    
    def initUI(self):
        self.parent.title("Blackhole")
        self.pack(fill=BOTH, expand=1)
        startMusicButton = Button(self, text = "Включить",
                                  background="#EEEEEE",
                                  font="20",
                                  command = lambda: (Music.start(Music)))
        startMusicButton.grid(row=0, column=0)
        pauseMusicButton = Button(self, text = "Пауза/Возобновить",
                                  background="#EEEEEE",
                                  font="20",
                                  command = lambda: (player.pause()))
        pauseMusicButton.grid(row=0, column=1)
        prevMusicButton = Button(self, text = "Предыдущий трек",
                                  background="#EEEEEE",
                                  font="20",
                                  command = lambda: (Music.next(Music, True)))
        prevMusicButton.grid(row=0, column=2)
        nextMusicButton = Button(self, text = "Следующий трек",
                                  background="#EEEEEE",
                                  font="20",
                                  command = lambda: (Music.next(Music, False)))
        nextMusicButton.grid(row=0, column=3)
        stopMusicButton = Button(self, text = "Выключить",
                                  background="#EEEEEE",
                                  font="20",
                                  command = lambda: (player.stop()))
        stopMusicButton.grid(row=0, column=4)
        randomCheck = Checkbutton(self, text='Перемешать треки',
                                  variable = Music.random_song,
                                  onvalue = True,
                                  offvalue = False,
                                  command = lambda: (Music.change_random(Music, 1)))
        randomCheck.grid(row = 0, column = 5)

    def centerWindow(self):
        w = 1080
        h = 480
 
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
 
        x = (sw - w) / 2
        y = (sh - h) / 2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

class Music():
    song_name = ''
    random_song = False
    ext_list = ['.mp3', '.wav', '.ogg']
    
    def change_random(self, bool_value):
        self.random_song = not self.random_song

    def switch_file(filepath, prev):
        directory = os.path.dirname(filepath)
        filename = os.path.basename(filepath)
        fileList = os.listdir(directory)
        if prev: nextIndex = fileList.index(filename) - 1
        else: nextIndex = fileList.index(filename) + 1
        print("Сейчас играет:", fileList[nextIndex])
        if nextIndex == len(fileList):
            nextIndex = 0
        path = directory + '/' + fileList[nextIndex]
        return path
    
    def random_file(self, filepath, prev):
        directory = os.path.dirname(filepath)
        filename = os.path.basename(filepath)
        fileList = os.listdir(directory)
        if prev: nextIndex = fileList.index(filename) - 1
        else: nextIndex = random.randint(0, len(fileList) - 1)
        print("Сейчас играет:", fileList[nextIndex])
        path = directory + '/' + fileList[nextIndex]
        if path == filepath: self.random_file(self, filepath)
        return path

    def start(self):
        self.song_name = fd.askopenfilename(title = 'Выберите музыку')
        Media = Instance.media_new(self.song_name)
        Media.get_mrl()
        player.set_media(Media)
        player.play() 
        player.audio_set_volume(70)

    def next(self, prev):
        Music.skip_not_music(self, prev)
        Media = Instance.media_new(self.song_name)
        Media.get_mrl()
        player.set_media(Media)
        player.play() 
        player.audio_set_volume(70)

    def skip_not_music(self, prev):
        if self.random_song:
            self.song_name = self.random_file(self, self.song_name, prev)
        else:
            self.song_name = self.switch_file(self.song_name, prev)
        ext = os.path.splitext(self.song_name)[-1].lower()
        if ext not in self.ext_list:
            self.next(self, prev)

def main():
    root = Tk()
    root.geometry("350x350+400+400")
    app = Example(root)
    root.mainloop()  
 
if __name__ == '__main__':
    main()