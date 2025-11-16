import pygame
from .player import Player
from .starfield import Starfield


class Game:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Buat background bintang
        self.starfield = Starfield(screen_width, screen_height, star_count=100)

        # Buat player di bawah tengah layar
        self.player = Player(
            x=screen_width / 2,
            y=screen_height - 60,
            speed=300,
            screen_width=screen_width,
        )

        self.background_color = (5, 5, 20)

    def handle_event(self, event: pygame.event.Event):
        # Tahap 1: belum ada event khusus selain QUIT di main loop
        # Method ini tetap disediakan agar nanti mudah diperluas.
        pass

    def update(self, dt: float):
        self.starfield.update(dt)
        self.player.update(dt)

    def draw(self, surface: pygame.Surface):
        surface.fill(self.background_color)
        self.starfield.draw(surface)
        self.player.draw(surface)
