# oop-galaxy-runner-02-python

## Capaian Pembelajaran

Mahasiswa diharapkan mampu:

1. Memodelkan permainan 2D sederhana menggunakan **pemrograman berorientasi objek** (class, object, composition, encapsulation, inheritance, polymorphism) di Python.
2. Menggunakan **PyGame** untuk membangun game 2D dengan beberapa komponen: player, musuh (enemy), background, skor, dan UI dasar.
3. Menerapkan **multimedia** (gambar, sprite animation, suara) di dalam game.
4. Mengelola **beberapa screen** (main menu, game screen, high score) menggunakan Screen Manager berbasis OOP.
5. Menerapkan **perilaku AI sederhana** pada musuh (enemy) dan mengatur tingkat kesulitan permainan.

---

## Lingkungan Pengembangan

1. Platform: Python **3.12+** (boleh 3.13 selama PyGame berjalan)
2. Bahasa: Python
3. Editor/IDE yang disarankan:

   * VS Code + Python Extension
   * Terminal
4. Library:

   * `pygame 2.6.1`
   * `pytest`

---

## Cara Menjalankan Project

```bash
python -m src.main
```

---

# Tahap 2 — Enemy, Collision, Encapsulation, Properties & Validation

**Tujuan Tahap 2**

1. Menambahkan **musuh (Enemy)** yang jatuh dari atas layar.
2. Menambahkan **score** dan **lives** pada `Player` dengan **encapsulation + property**.
3. Mengimplementasikan **collision detection** antara `Player` dan `Enemy`.
4. Mengatur logika sederhana:

   * Enemy lolos (turun sampai bawah) → **score bertambah**.
   * Enemy menabrak player → **lives berkurang**.

Struktur folder tetap seperti Tahap 1, hanya menambah **1 file baru**:

```text
src/
└─ core/
   ├─ player.py        # kita modifikasi sedikit
   ├─ starfield.py     # tetap
   ├─ game.py          # kita modifikasi
   └─ enemy.py         # BARU
```

---

## 1. Memperluas Player dengan Score & Lives (Encapsulation + Property)

Saat ini `Player` hanya mengatur posisi dan gambar pesawat.
Di Tahap 2, `Player` juga harus menyimpan **score** dan **jumlah nyawa (lives)**.

Beberapa hail yang perlu diperhatikan:

* Nilai `score` dan `lives` tidak boleh diubah sembarangan tanpa kontrol.
* Kita ingin memastikan nilainya **tidak negatif**.

Jadi kita data menggunakan:

* field internal: `_score`, `_lives`
* property: `score`, `lives` (dengan setter yang punya validasi)
* method helper: `add_score()`, `lose_life()`, `is_dead()`

---

### 1.1. Ubah constructor `Player`

**File:** `src/core/player.py`
Cari `__init__` di class `Player`.

Tambahkan **parameter** `lives: int = 3` dan field internal seperti ini:

```python
class Player:
    def __init__(self, x: float, y: float, speed: float, screen_width: int, lives: int = 3):
        self.x = x
        self.y = y
        self.speed = speed
        self.screen_width = screen_width

        self.width = 40
        self.height = 25
        self.color = (0, 220, 180)

        # Tambahkan state terenkapsulasi
        self._score = 0
        self._lives = lives
```

> Pastikan pemanggilan `Player(...)` di `Game` nanti kita update supaya mengirimkan argumen `lives=`.

---

### 1.2. Tambahkan property `score` dan `lives`

Masih di `player.py`, **tepat di bawah `__init__`**, tambahkan:

```python
    @property
    def score(self) -> int:
        return self._score

    @score.setter
    def score(self, value: int):
        if value < 0:
            raise ValueError("Score tidak boleh negatif.")
        self._score = int(value)

    @property
    def lives(self) -> int:
        return self._lives

    @lives.setter
    def lives(self, value: int):
        if value < 0:
            raise ValueError("Lives tidak boleh negatif.")
        self._lives = int(value)
```

---

### 1.3. Tambahkan method helper: `add_score`, `lose_life`, `is_dead`

Masih di `player.py`, **tepat di bawah property** tadi, tambahkan:

```python
    def add_score(self, points: int):
        if points < 0:
            raise ValueError("Penambahan score tidak boleh negatif.")
        self.score = self.score + points

    def lose_life(self, amount: int = 1):
        if amount < 0:
            raise ValueError("Pengurangan nyawa tidak boleh negatif.")
        new_lives = self.lives - amount
        if new_lives < 0:
            new_lives = 0
        self.lives = new_lives

    def is_dead(self) -> bool:
        return self.lives <= 0
```

> Nanti Tahap 3–5 kita bisa manfaatkan `is_dead()` untuk Game Over, dsb.

---

## 2. Menambahkan Class Enemy

Sekarang kita membuat musuh (`Enemy`) yang:

* muncul di atas layar,
* jatuh ke bawah,
* jika keluar layar → respawn di atas & **score bertambah**,
* jika menabrak player → player **kehilangan 1 nyawa**, enemy respawn.

---

### 2.1. Buat file baru `enemy.py`

**File baru:** `src/core/enemy.py`

Tulis kode berikut secara bertahap:

```python
import pygame
import random


class Enemy:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.width = 30
        self.height = 30
        self.color = (220, 60, 60)

        self.speed_min = 120
        self.speed_max = 260

        # Inisialisasi posisi awal
        self.reset()

    def reset(self):
        """Spawn enemy di posisi acak di atas layar."""
        self.x = random.randint(0, self.screen_width)
        self.y = -self.height
        self.speed = random.uniform(self.speed_min, self.speed_max)

    def update(self, dt: float):
        """Gerakkan enemy ke bawah."""
        self.y += self.speed * dt

    def is_off_screen(self) -> bool:
        """True jika enemy sudah lewat bawah layar."""
        return self.y > self.screen_height + self.height

    def get_rect(self) -> pygame.Rect:
        rect = pygame.Rect(0, 0, self.width, self.height)
        rect.centerx = int(self.x)
        rect.centery = int(self.y)
        return rect

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.color, self.get_rect())
```

---

## 3. Mengintegrasikan Enemy ke dalam Game

Hubungkan semuanya di kelas `Game`:

* `Game` punya **list of enemies**
* `update()`:

  * update semua enemy,
  * jika enemy keluar layar → respawn + `player.add_score(10)`,
* cek collision di method `_check_collisions()`.

---

### 3.1. Import Enemy di `game.py`

**File:** `src/core/game.py`
Di bagian import paling atas, tambahkan:

```python
from .enemy import Enemy
```

---

### 3.2. Tambahkan list `enemies` di constructor `Game`

Cari `__init__` di class `Game`.
Setelah inisialisasi `self.player = Player(...)`, tambahkan:

```python
        # Buat beberapa enemy
        self.enemies: list[Enemy] = []
        self.enemy_count = 5
        self._create_enemies()
```

Lalu, **masih di dalam class `Game`**, tambahkan method helper berikut (misalnya di bawah `__init__`):

```python
    def _create_enemies(self):
        self.enemies.clear()
        for _ in range(self.enemy_count):
            self.enemies.append(Enemy(self.screen_width, self.screen_height))
```

Jangan lupa juga ubah pemanggilan `Player` di `__init__` agar sesuai dengan constructor baru (yang punya `lives`):

```python
        self.player = Player(
            x=screen_width / 2,
            y=screen_height - 60,
            speed=300,
            screen_width=screen_width,
            lives=3,   # tambahkan ini
        )
```

---

### 3.3. Update method `update()` di `Game`

Masih di `src/core/game.py`, cari method `update(self, dt: float)`.

Sebelumnya cuma:

```python
    def update(self, dt: float):
        self.starfield.update(dt)
        self.player.update(dt)
```

Sekarang perlu ditambah logic untuk enemy dan collision.
Ubahlah jadi seperti ini:

```python
    def update(self, dt: float):
        self.starfield.update(dt)
        self.player.update(dt)

        # Update semua musuh
        for enemy in self.enemies:
            enemy.update(dt)

            # Jika enemy lewat bawah layar → respawn + tambah score
            if enemy.is_off_screen():
                enemy.reset()
                self.player.add_score(10)

        # Cek tabrakan antara player dan enemy
        self._check_collisions()
```

---

### 3.4. Tambahkan method `_check_collisions()` di `Game`

Di dalam class `Game`, tambahkan method baru ini (misalnya di bawah `update()`):

```python
    def _check_collisions(self):
        player_rect = self.player.get_rect()

        for enemy in self.enemies:
            if player_rect.colliderect(enemy.get_rect()):
                # Jika tabrakan:
                # 1. kurangi nyawa player
                # 2. respawn enemy
                self.player.lose_life(1)
                enemy.reset()
```

> Di sini kita memanfaatkan method `get_rect()` yang sebelumnya sudah ada di `Player` (Tahap 1).

---

### 3.5. Tambahkan HUD (Score & Lives)

Masih di `game.py`, kita ingin menampilkan score dan lives di kiri atas.

#### a) Inisialisasi font di `__init__`

Di akhir `__init__`, tambahkan:

```python
        pygame.font.init()
        self.hud_font = pygame.font.SysFont(None, 24)
```

#### b) Tambahkan method `_draw_hud`

Masih di dalam class `Game`, tambahkan:

```python
    def _draw_hud(self, surface: pygame.Surface):
        score_text = self.hud_font.render(f"Score: {self.player.score}", True, (255, 255, 255))
        lives_text = self.hud_font.render(f"Lives: {self.player.lives}", True, (255, 80, 80))

        surface.blit(score_text, (10, 10))
        surface.blit(lives_text, (10, 30))
```

#### c) Panggil `_draw_hud` di `draw()`

Cari method `draw(self, surface)` yang sebelumnya hanya menggambar starfield & player.
Tambahkan pemanggilan HUD di akhir:

```python
    def draw(self, surface: pygame.Surface):
        surface.fill(self.background_color)
        self.starfield.draw(surface)

        for enemy in self.enemies:
            enemy.draw(surface)

        self.player.draw(surface)

        # Tambahkan HUD
        self._draw_hud(surface)
```

---

## 4. Menjalankan Game (Tahap 2)

Tidak ada perubahan di `main.py`, jadi cukup jalankan:

```bash
python -m src.main
```

Seharusnya sekarang:

* Bintang tetap bergerak.
* Kapal player bisa bergerak kiri–kanan (arrow keys).
* Musuh merah jatuh dari atas (ada beberapa).
* Jika musuh **lewat bawah**, maka score di pojok kiri atas **bertambah**.
* Jika musuh **menabrak player**, maka lives **berkurang**.

> Jika `lives` sudah 0, saat ini game belum “game over visual”. Fitur Game Over akan dikerjakan pada tahap berikutnya.

---
