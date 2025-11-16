# tests/test_enemy.py
import pygame
import pytest

from src.core.enemy import Enemy


@pytest.fixture(scope="module", autouse=True)
def pygame_init():
    pygame.init()
    yield
    pygame.quit()


def test_enemy_reset_sets_position_above_screen():
    width, height = 800, 600
    enemy = Enemy(screen_width=width, screen_height=height)

    # Setelah __init__, reset() sudah dipanggil
    assert 0 <= enemy.x <= width
    # y di atas layar (negatif atau -height)
    assert enemy.y <= 0


def test_enemy_moves_down_on_update():
    width, height = 800, 600
    enemy = Enemy(screen_width=width, screen_height=height)

    # Set posisi & speed manual supaya deterministik
    enemy.y = 0
    enemy.speed = 100.0
    dt = 0.5  # 0.5 detik

    enemy.update(dt)

    # y harus bertambah sebesar speed * dt = 50
    assert enemy.y == pytest.approx(50.0)


def test_enemy_is_off_screen_when_past_bottom():
    width, height = 800, 600
    enemy = Enemy(screen_width=width, screen_height=height)

    enemy.y = height + enemy.height + 10  # jauh di bawah layar

    assert enemy.is_off_screen() is True


def test_enemy_is_not_off_screen_inside_bounds():
    width, height = 800, 600
    enemy = Enemy(screen_width=width, screen_height=height)

    enemy.y = height - 10  # masih sedikit di atas bottom

    assert enemy.is_off_screen() is False
