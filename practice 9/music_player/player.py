import os
import pygame


class MusicPlayer:
    def __init__(self, music_folder):
        self.music_folder = music_folder
        self.playlist = self.load_tracks()
        self.current_index = 0
        self.is_playing = False

        pygame.mixer.init()
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 32)

        print("Music folder:", self.music_folder)
        print("Playlist:", self.playlist)

        if self.playlist:
            self.load_current_track()

    def load_tracks(self):
        tracks = []

        if os.path.exists(self.music_folder):
            for file in os.listdir(self.music_folder):
                if file.lower().endswith(".mp3") or file.lower().endswith(".wav"):
                    tracks.append(file)

        tracks.sort()
        return tracks

    def load_current_track(self):
        if self.playlist:
            track_path = os.path.join(self.music_folder, self.playlist[self.current_index])
            pygame.mixer.music.load(track_path)

    def play(self):
        if self.playlist:
            pygame.mixer.music.play()
            self.is_playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def next_track(self):
        if self.playlist:
            self.current_index = (self.current_index + 1) % len(self.playlist)
            self.load_current_track()
            self.play()

    def previous_track(self):
        if self.playlist:
            self.current_index = (self.current_index - 1) % len(self.playlist)
            self.load_current_track()
            self.play()

    def get_current_track_name(self):
        if self.playlist:
            return self.playlist[self.current_index]
        return "No tracks found"

    def draw(self, screen):
        screen.fill((255, 255, 255))

        title = self.font.render("Music Player", True, (0, 0, 0))
        screen.blit(title, (20, 20))

        track_text = self.font.render(
            f"Current track: {self.get_current_track_name()}",
            True,
            (0, 0, 0)
        )
        screen.blit(track_text, (20, 80))

        status = "Playing" if self.is_playing else "Stopped"
        status_text = self.font.render(f"Status: {status}", True, (0, 0, 0))
        screen.blit(status_text, (20, 130))

        controls_1 = self.font.render("P = Play", True, (0, 0, 0))
        controls_2 = self.font.render("S = Stop", True, (0, 0, 0))
        controls_3 = self.font.render("N = Next", True, (0, 0, 0))
        controls_4 = self.font.render("B = Back", True, (0, 0, 0))
        controls_5 = self.font.render("Q = Quit", True, (0, 0, 0))

        screen.blit(controls_1, (20, 220))
        screen.blit(controls_2, (20, 260))
        screen.blit(controls_3, (20, 300))
        screen.blit(controls_4, (20, 340))
        screen.blit(controls_5, (20, 380))