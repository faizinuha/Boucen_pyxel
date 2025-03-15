import pyxel

class Game:
    def __init__(self):
        self.level = 1
        self.reset_game()

    def update(self, skin):
        if self.game_over or self.win:
            if pyxel.btnp(pyxel.KEY_R):
                self.reset_game()
                self.game_over = False
                self.win = False
            elif pyxel.btnp(pyxel.KEY_M):
                return "menu"
            elif pyxel.btnp(pyxel.KEY_L):
                return "leaderboard"
            return None

        # Gerakan bola
        self.ball_speed_y += self.gravity
        self.ball_x += self.ball_speed_x
        self.ball_y += self.ball_speed_y

        # Kontrol bola
        if pyxel.btn(pyxel.KEY_LEFT):
            self.ball_x -= 2
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.ball_x += 2
        if pyxel.btnp(pyxel.KEY_SPACE) and not self.is_jumping:
            self.ball_speed_y = -5
            self.is_jumping = True

        # Batas kiri
        if self.ball_x < 0:
            self.ball_x = 0

        # Cek tabrakan dengan platform
        self.is_jumping = True
        for platform in self.platforms:
            if (
                self.ball_x + 4 >= platform[0]
                and self.ball_x - 4 <= platform[0] + platform[2]
                and self.ball_y + 4 >= platform[1]
                and self.ball_y - 4 <= platform[1] + platform[3]
                and self.ball_speed_y > 0
            ):
                self.ball_y = platform[1] - 4
                self.ball_speed_y = 0
                self.is_jumping = False

        # Cek tabrakan dengan musuh
        for enemy in self.enemies:
            if (
                self.ball_x + 4 >= enemy[0]
                and self.ball_x - 4 <= enemy[0] + enemy[2]
                and self.ball_y + 4 >= enemy[1]
                and self.ball_y - 4 <= enemy[1] + enemy[3]
            ):
                self.game_over = True
                return "lose_life"

        # Cek tabrakan dengan finish
        if (
            self.ball_x + 4 >= self.finish[0]
            and self.ball_x - 4 <= self.finish[0] + self.finish[2]
            and self.ball_y + 4 >= self.finish[1]
            and self.ball_y - 4 <= self.finish[1] + self.finish[3]
        ):
            self.win = True
            self.total_score += 100  # Tambah skor
            self.level += 1  # Naik level
            self.reset_game()

        return None

    def draw(self, skin):
        pyxel.cls(0)
        # pyxel.blt(0, 0, 0, 0, 0, 160, 120)  # Draw background image

        # Gambar platform, musuh, finish, dan bola
        for platform in self.platforms:
            pyxel.rect(platform[0], platform[1], platform[2], platform[3], 3)
        for enemy in self.enemies:
            pyxel.circ(enemy[0] + enemy[2] // 2, enemy[1] + enemy[3] // 2, enemy[2] // 2, 8)
        pyxel.rect(self.finish[0], self.finish[1], self.finish[2], self.finish[3], 10)
        pyxel.circ(self.ball_x, self.ball_y, 4, skin)  # Gunakan skin yang dipilih

        if self.game_over:
            pyxel.text(50, 50, "GAME OVER", 8)
            pyxel.text(50, 60, "R: Ulang", 7)
            pyxel.text(50, 70, "M: Menu", 7)
            pyxel.text(50, 80, "L: Leaderboard", 7)
        if self.win:
            pyxel.text(50, 50, "YOU WIN!", 11)
            pyxel.text(50, 60, f"Skor: {self.total_score}", 7)
            pyxel.text(50, 70, "R: Ulang", 7)
            pyxel.text(50, 80, "M: Menu", 7)
            pyxel.text(50, 90, "L: Leaderboard", 7)

    def reset_game(self):
        self.ball_x = 10  # Start at the back line
        self.ball_y = 100
        self.ball_speed_x = 0
        self.ball_speed_y = 0
        self.gravity = 0.3
        self.is_jumping = False
        if self.level == 1:
            self.platforms = [(0, 110, 160, 10), (40, 80, 80, 10), (100, 50, 60, 10)]  # (x, y, width, height)
            self.enemies = [(60, 90, 10, 10), (120, 40, 10, 10)]  # (x, y, width, height)
            self.finish = (150, 20, 10, 10)  # (x, y, width, height)
        elif self.level == 2:
            self.platforms = [(0, 110, 160, 10), (30, 90, 100, 10), (80, 60, 80, 10)]  # (x, y, width, height)
            self.enemies = [(50, 80, 10, 10), (110, 50, 10, 10)]  # (x, y, width, height)
            self.finish = (140, 30, 10, 10)  # (x, y, width, height)
        elif self.level == 3:
            self.platforms = [(0, 110, 160, 10), (20, 100, 120, 10), (60, 70, 100, 10)]  # (x, y, width, height)
            self.enemies = [(40, 90, 10, 10), (90, 60, 10, 10)]  # (x, y, width, height)
            self.finish = (130, 40, 10, 10)  # (x, y, width, height)
        self.game_over = False
        self.win = False
        self.total_score = 0