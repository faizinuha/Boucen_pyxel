import pygame

class Leaderboard:
    def __init__(self):
        self.scores = []

    def add_score(self, name, score):
        self.scores.append((name, score))
        self.scores.sort(key=lambda x: x[1], reverse=True)  # Sort by score (highest first)

    def update(self):
        if pygame.key.get_pressed()[pygame.K_BACKSPACE]:
            return "menu"
        return None

    def draw(self, screen):
        font = pygame.font.SysFont(None, 24)
        text = font.render("Leaderboard", True, (255, 255, 255))
        screen.blit(text, (50, 30))
        for i, (name, score) in enumerate(self.scores[:5]):  # Display top 5
            text = font.render(f"{name}: {score}", True, (255, 255, 255))
            screen.blit(text, (50, 50 + i * 10))
        text = font.render("Backspace: Kembali", True, (255, 255, 255))
        screen.blit(text, (50, 100))