import pygame
from tkinter.filedialog import *
from tkinter import *


pygame.init()
import db

class FrameApp(Toplevel):
    def __init__(self, master, **kwargs):
        super().__init__(**kwargs)
        self.paused = False
        self.master = master
        self.playlist = list()
        self.actual_song = 0
        self.b1 = Button(self, text="play", command=self.play_music, width=20)
        self.b1.pack()
        self.b2 = Button(self, text="previous", command=self.previous_song,
                         width=20)
        self.q = Button(self, command = self.master.get_user_id)
        self.b2.pack()
        self.b3 = Button(self, text="pause", command=self.toggle, width=20)
        self.b3.pack()
        self.liked = False
        self.b4 = Button(self, text="next", command=self.next_song, width=20)
        self.b4.pack()

        self.b5 = Button(self, text='like', command=self.like, width=20)
        self.b5.pack()


        self.label1 = Label(self)
        self.label1.pack()
        self.END_MUSIC_EVENT = pygame.USEREVENT + 0
        self.add_to_list()
        self.play_music()
        self.check_music()
        # TODO: Make progressbar, delete songs from playlist, amplify volume

    def like(self):
        if self.liked:
            self.liked = False
        else:
            user_id = db.get_user_id(self.master.username.get())
            self.liked = True
            track = self.playlist[self.actual_song]
            track = track[75:-5]
            if track.find('\'') == 1:
                track = track[:track.index('\'')] + '\'' + track[track.index('\''):]
            print(f'User_id:{user_id} Track:{track}')
            db.set_like(user_id, track)

    def add_to_list(self):
        user_id = db.get_user_id(self.master.username.get())
        directory = db.get_songs_list(user_id)
        # appends song directory on disk to playlist in memory
        for song_dir in directory:
            self.playlist.append(song_dir)

    def play_music(self):
        self.like = False
        pygame.mixer.music.set_volume(0.3)
        print(f'Playlist: {self.playlist}')
        directory = self.playlist[self.actual_song]
        pygame.mixer.music.load(directory)
        pygame.mixer.music.play(1, 0.0)
        pygame.mixer.music.set_endevent(self.END_MUSIC_EVENT)
        self.check_music()

    def check_music(self):
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                self.destroy()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.next_song()
            elif event.type == self.MUSIC_ENDED:
                self.next_song()
    def toggle(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
        elif not self.paused:
            pygame.mixer.music.pause()
            self.paused = True

    def get_next_song(self):
        if self.actual_song + 2 <= len(self.playlist):
            return self.actual_song + 1
        else:
            return 0

    def next_song(self):
        self.liked = False
        self.actual_song = self.get_next_song()
        self.play_music()

    def get_previous_song(self):
        """
        Gets previous song number on playlist and returns it
        :return: int - prevoius song number on playlist
        """
        if self.actual_song - 1 >= 0:
            return self.actual_song - 1
        else:
            return len(self.playlist) - 1

    def previous_song(self):
        """
        Plays prevoius song
        :return:
        """
        self.actual_song = self.get_previous_song()
        self.play_music()


