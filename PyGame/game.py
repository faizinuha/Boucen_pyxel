import pygame

class Game:
    def __init__(self):
        self.level = 1
        self.reset_game()

    def update(self, skin):
        keys = pygame.key.get_pressed()
        if self.game_over or self.win:
            if keys[pygame.K_r]:
                self.reset_game()
                self.game_over = False
                self.win = False
            elif keys[pygame.K_m]:
                return "menu"
            elif keys[pygame.K_l]:
                return "leaderboard"
            return None

        # Ball movement
        self.ball_speed_y += self.gravity
        self.ball_x += self.ball_speed_x
        self.ball_y += self.ball_speed_y

        # Ball control
        if keys[pygame.K_LEFT]:
            self.ball_x -= 2
        if keys[pygame.K_RIGHT]:
            self.ball_x += 2
        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.ball_speed_y = -5
            self.is_jumping = True

        # Left boundary
        if self.ball_x < 0:
            self.ball_x = 0

        # Check collision with platform
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

        # Check collision with enemy
        for enemy in self.enemies:
            if (
                self.ball_x + 4 >= enemy[0]
                and self.ball_x - 4 <= enemy[0] + enemy[2]
                and self.ball_y + 4 >= enemy[1]
                and self.ball_y - 4 <= enemy[1] + enemy[3]
            ):
                self.game_over = True
                return "lose_life"

        # Check collision with finish
        if (
            self.ball_x + 4 >= self.finish[0]
            and self.ball_x - 4 <= self.finish[0] + self.finish[2]
            and self.ball_y + 4 >= self.finish[1]
            and self.ball_y - 4 <= self.finish[1] + self.finish[3]
        ):
            self.win = True
            self.total_score += 100  # Add score
            self.level += 1  # Level up
            self.reset_game()

        return None

    def draw(self, screen, skin):
        screen.fill((0, 0, 0))

        # Draw platforms, enemies, finish, and ball
        for platform in self.platforms:
            pygame.draw.rect(screen, (0, 255, 0), platform)
        for enemy in self.enemies:
            pygame.draw.circle(screen, (255, 0, 0), (enemy[0] + enemy[2] // 2, enemy[1] + enemy[3] // 2), enemy[2] // 2)
        pygame.draw.rect(screen, (0, 0, 255), self.finish)
        pygame.draw.circle(screen, skin, (self.ball_x, self.ball_y), 4)

        if self.game_over:
            font = pygame.font.SysFont(None, 24)
            text = font.render("GAME OVER", True, (255, 0, 0))
            screen.blit(text, (50, 50))
            text = font.render("R: Ulang", True, (255, 255, 255))
            screen.blit(text, (50, 60))
            text = font.render("M: Menu", True, (255, 255, 255))
            screen.blit(text, (50, 70))
            text = font.render("L: Leaderboard", True, (255, 255, 255))
            screen.blit(text, (50, 80))
        if self.win:
            font = pygame.font.SysFont(None, 24)
            text = font.render("YOU WIN!", True, (0, 255, 0))
            screen.blit(text, (50, 50))
            text = font.render(f"Skor: {self.total_score}", True, (255, 255, 255))
            screen.blit(text, (50, 60))
            text = font.render("R: Ulang", True, (255, 255, 255))
            screen.blit(text, (50, 70))
            text = font.render("M: Menu", True, (255, 255, 255))
            screen.blit(text, (50, 80))
            text = font.render("L: Leaderboard", True, (255, 255, 255))
            screen.blit(text, (50, 90))

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