import pygame
from menu import Menu
from skin import Skin
from leaderboard import Leaderboard
from game import Game

class BounceModern:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((160, 120))
        pygame.display.set_caption("Selamat Datang Bounce...")
        self.clock = pygame.time.Clock()
        self.current_screen = "menu"
        self.menu = Menu()
        self.skin = Skin()
        self.leaderboard = Leaderboard()
        self.game = Game()
        self.current_skin = (255, 0, 0)  # Default skin (red)
        self.lives = 3  # Initialize lives
        self.running = True
        self.main_loop()

    def main_loop(self):
        while self.running:
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        if self.current_screen == "menu":
            choice = self.menu.update()
            if choice == "play":
                self.current_screen = "game"
            elif choice == "skin":
                self.current_screen = "skin"
            elif choice == "leaderboard":
                self.current_screen = "leaderboard"
            elif choice == "quit":
                self.running = False

        elif self.current_screen == "skin":
            skin_choice = self.skin.update()
            if skin_choice:
                self.current_skin = skin_choice
                self.current_screen = "menu"

        elif self.current_screen == "leaderboard":
            if pygame.key.get_pressed()[pygame.K_BACKSPACE]:
                self.current_screen = "menu"

        elif self.current_screen == "game":
            result = self.game.update(self.current_skin)
            if result == "menu":
                self.current_screen = "menu"
            elif result == "leaderboard":
                self.leaderboard.add_score("Player", self.game.total_score)  # Add total score to leaderboard
                self.current_screen = "leaderboard"
            elif result == "lose_life":
                self.lives -= 1
                if self.lives > 0:
                    self.game.reset_game()
                else:
                    self.current_screen = "game_over"

        elif self.current_screen == "game_over":
            if pygame.key.get_pressed()[pygame.K_r]:
                self.lives = 3  # Reset lives
                self.game.reset_game()
                self.current_screen = "game"
            elif pygame.key.get_pressed()[pygame.K_m]:
                self.current_screen = "menu"

    def draw(self):
        self.screen.fill((0, 0, 0))
        if self.current_screen == "menu":
            self.menu.draw(self.screen)
        elif self.current_screen == "skin":
            self.skin.draw(self.screen)
        elif self.current_screen == "leaderboard":
            self.leaderboard.draw(self.screen)
        elif self.current_screen == "game":
            self.game.draw(self.screen, self.current_skin)
            font = pygame.font.SysFont(None, 24)
            text = font.render(f"Nyawa: {self.lives}", True, (255, 255, 255))
            self.screen.blit(text, (5, 5))
        elif self.current_screen == "game_over":
            font = pygame.font.SysFont(None, 24)
            text = font.render("GAME OVER", True, (255, 0, 0))
            self.screen.blit(text, (50, 50))
            text = font.render("R: Ulang", True, (255, 255, 255))
            self.screen.blit(text, (50, 60))
            text = font.render("M: Menu", True, (255, 255, 255))
            self.screen.blit(text, (50, 70))

BounceModern()