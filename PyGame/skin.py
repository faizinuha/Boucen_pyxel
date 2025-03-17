import pygame

class Skin:
    def __init__(self):
        pass

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            return (255, 0, 0)  # Red
        elif keys[pygame.K_2]:
            return (0, 255, 0)  # Green
        elif keys[pygame.K_3]:
            return (255, 255, 0)  # Yellow
        elif keys[pygame.K_9]:
            return None  # Back
        return None

    def draw(self, screen):
        font = pygame.font.SysFont(None, 24)
        text = font.render("Pilih Skin", True, (255, 255, 255))
        screen.blit(text, (50, 30))
        text = font.render("1. Merah", True, (255, 0, 0))
        screen.blit(text, (50, 50))
        text = font.render("2. Hijau", True, (0, 255, 0))
        screen.blit(text, (50, 60))
        text = font.render("3. Kuning", True, (255, 255, 0))
        screen.blit(text, (50, 70))
        text = font.render("9: Kembali", True, (255, 255, 255))
        screen.blit(text, (50, 80))