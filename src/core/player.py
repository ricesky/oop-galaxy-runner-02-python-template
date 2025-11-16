import pygame


class Player:
    def __init__(self, x: float, y: float, speed: float, screen_width: int):
        self.x = x
        self.y = y
        self.speed = speed
        self.screen_width = screen_width

        # Ukuran kapal
        self.width = 40
        self.height = 25

        # Warna kapal (hijau kebiruan)
        self.color = (0, 220, 180)

    def handle_input(self, dt: float):
        keys = pygame.key.get_pressed()
        dx = 0

        if keys[pygame.K_LEFT]:
            dx -= self.speed * dt
        if keys[pygame.K_RIGHT]:
            dx += self.speed * dt

        self.x += dx

        # Batasi supaya tidak keluar layar
        half_w = self.width / 2
        if self.x < half_w:
            self.x = half_w
        if self.x > self.screen_width - half_w:
            self.x = self.screen_width - half_w

    def update(self, dt: float):
        # Untuk tahap 1, tidak ada update lain.
        # Method ini tetap disediakan agar nanti mudah diperluas.
        self.handle_input(dt)

    def draw(self, surface: pygame.Surface):
        # Gambar kapal sebagai persegi panjang
        rect = pygame.Rect(0, 0, self.width, self.height)
        rect.centerx = int(self.x)
        rect.centery = int(self.y)

        pygame.draw.rect(surface, self.color, rect)

        # Tambahan kecil: segitiga di depan agar terlihat seperti spaceship
        nose_points = [
            (rect.centerx, rect.top - 5),
            (rect.left, rect.top + 5),
            (rect.right, rect.top + 5),
        ]
        pygame.draw.polygon(surface, self.color, nose_points)
