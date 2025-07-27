import pyxel
from menu import Menu
from skin import Skin
from leaderboard import Leaderboard
from game import Game

class BounceModern:
    def __init__(self):
        pyxel.init(160, 120, title="Selamat Datang Bounce...")
        # pyxel.init(160, 120, caption="Bounce Modern")
        # pyxel.load("assets/music.pyxres")  # Load music resource - BARIS INI DIKOMENTARI
        self.current_screen = "menu"
        self.menu = Menu()
        self.skin = Skin()
        self.leaderboard = Leaderboard()
        self.game = Game() # Game diinisialisasi di sini, level pertama akan di-generate
        self.current_skin = 8  # Default skin (merah)
        self.lives = 3  # Initialize lives
        # pyxel.playm(0, loop=True)  # Play background music - BARIS INI JUGA DIKOMENTARI KARENA TIDAK ADA RESOURCE
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.current_screen == "menu":
            choice = self.menu.update()
            if choice == "play":
                self.game = Game() # Inisialisasi ulang game untuk memulai baru
                self.game._generate_level() # Generate level pertama secara eksplisit
                self.lives = 3 # Reset nyawa
                self.current_screen = "game"
            elif choice == "skin":
                self.current_screen = "skin"
            elif choice == "leaderboard":
                self.current_screen = "leaderboard"
            elif choice == "quit":
                pyxel.quit()

        elif self.current_screen == "skin":
            skin_choice = self.skin.update()
            if skin_choice:
                self.current_skin = skin_choice
                self.current_screen = "menu"

        elif self.current_screen == "leaderboard":
            if self.leaderboard.update() == "menu":
                self.current_screen = "menu"

        elif self.current_screen == "game":
            result = self.game.update(self.current_skin)
            if result == "menu":
                self.current_screen = "menu"
            elif result == "leaderboard":
                self.leaderboard.add_score("Player", self.game.total_score)
                self.current_screen = "leaderboard"
            elif result == "lose_life":
                self.lives -= 1
                if self.lives > 0:
                    self.game.reset_ball_position() # Hanya reset posisi bola, level tidak berubah
                else:
                    self.current_screen = "game_over"
            elif result == "game_complete":
                self.leaderboard.add_score("Player", self.game.total_score)
                self.current_screen = "leaderboard" # Langsung ke leaderboard setelah game selesai semua level
                self.game = Game() # Reset game state untuk play berikutnya
                self.lives = 3 # Reset nyawa

        elif self.current_screen == "game_over":
            if pyxel.btnp(pyxel.KEY_R):
                self.lives = 3
                self.game = Game() # Inisialisasi ulang game untuk memulai baru
                self.game._generate_level() # Generate level pertama secara eksplisit
                self.current_screen = "game"
            elif pyxel.btnp(pyxel.KEY_M):
                self.current_screen = "menu"

    def draw(self):
        pyxel.cls(0)
        if self.current_screen == "menu":
            self.menu.draw()
        elif self.current_screen == "skin":
            self.skin.draw()
        elif self.current_screen == "leaderboard":
            self.leaderboard.draw()
        elif self.current_screen == "game":
            self.game.draw(self.current_skin)
            pyxel.text(5, 5, f"Nyawa: {self.lives}", 7)
            pyxel.text(100, 5, f"Level: {self.game.level}", 7)
            pyxel.text(100, 15, f"Skor: {self.game.total_score}", 7)
        elif self.current_screen == "game_over":
            pyxel.text(50, 50, "GAME OVER", 8)
            pyxel.text(50, 60, "R: Ulang", 7)
            pyxel.text(50, 70, "M: Menu", 7)
            pyxel.text(50, 80, f"Skor Akhir: {self.game.total_score}", 7)

BounceModern()
