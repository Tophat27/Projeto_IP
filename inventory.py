# inventory.py
# Manages the player's inventory, including adding and using items.

import pygame
from variaveis import get_size
from items import Boots, Umbrella

largura, altura = get_size()

class Inventory:
    def __init__(self):
        self.items = {"Boots": 0, "Umbrella": 0}
        #self.slot_img = pygame.image.load("images/slot_inventario.png")
        #self.slot_img = pygame.transform.scale(self.slot_img, (largura // 8, altura // 8))
        self.fonte_pequena = pygame.font.SysFont("Arial", 30)

    def add_item(self, item_name):
        if item_name in self.items:
            self.items[item_name] += 1

    def use_item(self, item_name, player):
        if self.items[item_name] > 0:
            self.items[item_name] -= 1
            if item_name == "Boots":
                item = Boots()
            elif item_name == "Umbrella":
                item = Umbrella()
            item.use(player)
            return True
        return False

    def has_item(self, item_name):
        return self.items[item_name] > 0

    def draw(self, tela):
        pos_x = 20
        pos_y = altura - 100
        for i, (item_name, count) in enumerate(self.items.items()):
            #tela.blit(self.slot_img, (pos_x + i * (128 + 10), pos_y))
            if count > 0:
                text = self.fonte_pequena.render(f"{item_name}: {count}", True, (255, 255, 255))
                tela.blit(text, (pos_x + i * (128 + 10) + 10, pos_y + 10))