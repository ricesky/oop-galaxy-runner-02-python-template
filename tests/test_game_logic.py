# tests/test_game_logic.py
import pygame
import pytest

from src.core.game import Game
from src.core.enemy import Enemy


@pytest.fixture(scope="module", autouse=True)
def pygame_init():
    pygame.init()
    yield
    pygame.quit()


def make_game():
    return Game(screen_width=800, screen_height=600)


def test_enemy_off_screen_increases_player_score(monkeypatch):
    game = make_game()

    # Mulai dengan score 0
    game.player._score = 0  # atau gunakan add_score(0) kalau mau lebih "rapi"

    # Buat satu enemy yang sudah berada di bawah layar
    enemy = Enemy(game.screen_width, game.screen_height)
    enemy.y = game.screen_height + enemy.height + 5  # pasti off-screen

    # Pastikan enemy list hanya berisi 1 musuh ini
    game.enemies = [enemy]

    # Jalankan satu frame update
    dt = 0.016
    game.update(dt)

    # Setelah update: enemy.is_off_screen() True → enemy.reset() + add_score(10)
    assert game.player.score == 10


def test_collision_between_player_and_enemy_reduces_life(monkeypatch):
    game = make_game()

    # Set lives awal = 3
    game.player.lives = 3

    # Posisi player rect
    player_rect = game.player.get_rect()

    # Buat enemy yang PASTI bertabrakan dengan player
    enemy = Enemy(game.screen_width, game.screen_height)
    enemy.x = player_rect.centerx
    enemy.y = player_rect.centery

    game.enemies = [enemy]

    # Jalankan update
    dt = 0.016
    game.update(dt)

    # lives harus berkurang 1
    assert game.player.lives == 2


def test_enemy_reset_called_after_collision(monkeypatch):
    game = make_game()

    player_rect = game.player.get_rect()
    enemy = Enemy(game.screen_width, game.screen_height)
    enemy.x = player_rect.centerx
    enemy.y = player_rect.centery

    game.enemies = [enemy]

    # Pastikan reset() dipanggil
    called = {"reset": 0}

    def fake_reset():
        called["reset"] += 1

    # Monkeypatch method reset di enemy
    enemy.reset = fake_reset

    dt = 0.016
    game.update(dt)

    # Karena ada collision, reset() harus dipanggil tepat sekali
    assert called["reset"] == 1
