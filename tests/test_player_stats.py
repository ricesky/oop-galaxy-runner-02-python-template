# tests/test_player_stats.py
import pygame
import pytest

from src.core.player import Player


@pytest.fixture(scope="module", autouse=True)
def pygame_init():
    pygame.init()
    yield
    pygame.quit()


def make_player():
    # Helper supaya tidak mengulang argumen
    return Player(
        x=400,
        y=550,
        speed=300,
        screen_width=800,
        lives=3,
    )


def test_player_initial_score_and_lives():
    player = make_player()

    assert player.score == 0
    assert player.lives == 3


def test_player_score_cannot_be_negative_direct_set():
    player = make_player()

    with pytest.raises(ValueError):
        player.score = -10


def test_player_lives_cannot_be_negative_direct_set():
    player = make_player()

    with pytest.raises(ValueError):
        player.lives = -1


def test_add_score_increases_score():
    player = make_player()

    player.add_score(10)
    player.add_score(5)

    assert player.score == 15


def test_add_score_rejects_negative_points():
    player = make_player()

    with pytest.raises(ValueError):
        player.add_score(-5)


def test_lose_life_decreases_lives():
    player = make_player()
    assert player.lives == 3

    player.lose_life()
    assert player.lives == 2

    player.lose_life(2)
    assert player.lives == 0
    assert player.is_dead() is True


def test_lose_life_does_not_go_below_zero():
    player = make_player()
    assert player.lives == 3

    # Kurangi lebih besar dari nyawa yang ada
    player.lose_life(5)

    assert player.lives == 0
    assert player.is_dead() is True


def test_lose_life_rejects_negative_amount():
    player = make_player()

    with pytest.raises(ValueError):
        player.lose_life(-1)
