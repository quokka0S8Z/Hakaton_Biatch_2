import pygame
from Character import Character as char
class HealthBar(char):
    def __init__(self, player):
        self.player = player
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (20, 20, 200, 20))
        pygame.draw.rect(screen, (0, 255, 0), (20, 20, 2 * self.player.health, 20))
#moved to main cz why make those 2 lines so complicated
