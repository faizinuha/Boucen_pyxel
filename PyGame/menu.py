import pygame

class Menu:
    def __init__(self):
        pass

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            return "play"
        elif keys[pygame.K_2]:
            return "skin"
        elif keys[pygame.K_3]:
            return "leaderboard"
        elif keys[pygame.K_4]:
            return "quit"
        return None

    def draw(self, screen):
        font = pygame.font.SysFont(None, 24)
        text = font.render("Bounce Modern", True, (255, 255, 255))
        screen.blit(text, (50, 30))
        text = font.render("1. Main", True, (255, 255, 255))
        screen.blit(text, (50, 50))
        text = font.render("2. Pilih Skin", True, (255, 255, 255))
        screen.blit(text, (50, 60))
        text = font.render("3. Leaderboard", True, (255, 255, 255))
        screen.blit(text, (50, 70))
        text = font.render("4. Keluar", True, (255, 255, 255))
        screen.blit(text, (50, 80))