from tkinter import *
from tkinter import filedialog as fd
import os
import vlc
import random

Instance = vlc.Instance()
player = Instance.media_player_new()

after_id = ''

class Music():
    song_name = ''
    random_song = False
    ext_list = ['.mp3', '.wav', '.ogg']
    player_volume = 50

    def change_random(self):
        self.random_song = not self.random_song
        if self.random_song: prevMusicButton['state'] = 'disabled'
        else: prevMusicButton['state'] = 'active'

    def switch_file(filepath, prev):
        directory = os.path.dirname(filepath)
        filename = os.path.basename(filepath)
        fileList = os.listdir(directory)
        if prev: nextIndex = fileList.index(filename) - 1
        else: nextIndex = fileList.index(filename) + 1
        if nextIndex == len(fileList):
            nextIndex = 0
        nextpath = directory + '/' + fileList[nextIndex]
        return nextpath
    
    def random_file(self, filepath):
        directory = os.path.dirname(filepath)
        filename = os.path.basename(filepath)
        fileList = os.listdir(directory)
        nextIndex = random.randint(0, len(fileList) - 1)
        nextpath = directory + '/' + fileList[nextIndex]
        if nextpath == filepath: self.random_file(self, filepath)
        return nextpath

    def start_player(self):
        self.stop_player()

        self.song_name = fd.askopenfilename(title = 'Выберите музыку')
        nowPlaying['text'] = os.path.basename(self.song_name)
        Media = Instance.media_new(self.song_name)
        Media.get_mrl()
        player.set_media(Media)
        player.play() 
        player.audio_set_volume(self.player_volume)  

    def next_song(self, prev):
        Music.skip_not_music(self, prev)
        nowPlaying['text'] = os.path.basename(self.song_name)
        Media = Instance.media_new(self.song_name)
        Media.get_mrl()
        player.set_media(Media)
        player.play() 
        player.audio_set_volume(self.player_volume)

    def skip_not_music(self, prev):
        if self.random_song:
            self.song_name = self.random_file(self, self.song_name)
        else:
            self.song_name = self.switch_file(self.song_name, prev)
        ext = os.path.splitext(self.song_name)[-1].lower()
        if ext not in self.ext_list:
            self.next_song(self, prev)
    
    def change_volume(self, minus):
        if minus: 
            if self.player_volume - 10 >= 0: self.player_volume -= 10
        else: self.player_volume += 10
        volumeLabel['text'] = "Громкость: " + str(self.player_volume)
        player.audio_set_volume(self.player_volume)

    def stop_player():
        player.stop()
        nowPlaying["text"] = "Сейчас ничего не играет"

gui = Tk()
gui.geometry('500x250')
gui.configure(background = '#333333')
gui.resizable(width=True, height=False) 

frame_top = Frame(background = '#111111')
frame_mid = Frame(background = '#555555')

frame_midtop = Frame(frame_mid, background = '#555555')
frame_midmid = Frame(frame_mid, background = '#555555')
frame_midbot = Frame(frame_mid, background = '#555555')

startMusicButton = Button(frame_top, text = "Включить",
                            highlightthickness = 0, bd = 0,
                            background="#111111",
                            font=('Comic Sans MS', 20),
                            fg = '#EEEEEE',
                            command = lambda: (Music.start_player(Music)))
pauseMusicButton = Button(frame_midbot, text = "▍▍",
                            highlightthickness = 0, bd = 0,
                            background="#555555",
                            font=20,
                            fg = '#EEEEEE',
                            command = lambda: (player.pause()))
prevMusicButton = Button(frame_midbot, text = "🡸",
                            highlightthickness = 0, bd = 0,
                            background="#555555",
                            font = 20,
                            fg = '#EEEEEE',
                            command = lambda: (Music.next_song(Music, True)))
nextMusicButton = Button(frame_midbot, text = "🡺",
                            highlightthickness = 0, bd = 0,
                            background="#555555",
                            font = 20,
                            fg = '#EEEEEE',
                            command = lambda: (Music.next_song(Music, False)))
stopMusicButton = Button(frame_top, text = "Выключить",
                            highlightthickness = 0, bd = 0,
                            background="#111111",
                            font=('Comic Sans MS', 20),
                            fg = '#EEEEEE',
                            command = lambda: (Music.stop_player()))
randomCheck = Checkbutton(frame_top, text='Перемешать треки',
                            background = "#111111",
                            font=('Comic Sans MS', 10),
                            fg = '#EEEEEE',
                            command = lambda: (Music.change_random(Music)))
volumeScaleMinus = Button(frame_midmid, text = "-",
                            highlightthickness = 0, bd = 0,
                            background="#555555",
                            fg = '#EEEEEE',
                            font = 20,
                            command = lambda: (Music.change_volume(Music, True)))
volumeScalePlus= Button(frame_midmid, text = "+",
                            highlightthickness = 0, bd = 0,
                            background="#555555",
                            font = 20,
                            fg = '#EEEEEE',
                            command = lambda: (Music.change_volume(Music, False)))

volumeLabel = Label(frame_midmid, background = "#555555", text = 'Громкость: 50', font=('Comic Sans MS', 10), fg = '#EEEEEE')
nowPlaying = Label(frame_midtop, background = "#555555", text = 'Сейчас ничего не играет', font=('Comic Sans MS', 10), fg = '#EEEEEE', width = 200)

frame_top.pack(side = 'top', fill = 'both')
startMusicButton.pack(side = 'left')
stopMusicButton.pack(side = 'left')
randomCheck.pack(side = 'left')

frame_mid.pack(side = 'left')

frame_midtop.pack(side = 'top')
nowPlaying.pack(side = 'left', fill = 'x')

frame_midmid.pack(side = 'top')
volumeScaleMinus.pack(side = 'left')
volumeLabel.pack(side = 'left')
volumeScalePlus.pack(side = 'left')

frame_midbot.pack(side = 'top')
pauseMusicButton.pack(side = 'left')
prevMusicButton.pack(side = 'left')
nextMusicButton.pack(side = 'left')

gui.mainloop()