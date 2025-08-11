# enemy.py
# Manages enemy spawning and behavior.

import pygame
import random
from variaveis import get_size

largura, _ = get_size()

class Enemy:
    def __init__(self, hp=40):
        self.max_hp = hp
        self.hp = hp
        self.damage = random.randint(10, 30)  # 10-30% of player's max HP (100)
        self.image = pygame.image.load("images/enemy.png")  # Ensure you have an enemy.png
        self.image = pygame.transform.scale(self.image, (largura // 16, largura // 8))
        self.rect = self.image.get_rect(topleft=(0, 0))  # Spawn 100px from left, on ground

    def take_damage(self, damage):
        self.hp = max(0, self.hp - damage)

    def move(self, player_y):
        # Simple movement: stay on same x, adjust y to match player's y
        self.rect.y = player_y