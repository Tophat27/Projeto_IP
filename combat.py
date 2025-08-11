# combat.py
# Manages the turn-based combat system, including battle loop, player/enemy turns, and UI.

import pygame
import sys
from variaveis import get_size
from tela import tela

# Initializing screen for combat
largura, altura = get_size()
tela_combat = tela()

class CombatSystem:
    def __init__(self, player, enemy, inventory, fonte_grande, fonte_media):
        self.player = player
        self.enemy = enemy
        self.inventory = inventory
        self.fonte_grande = fonte_grande
        self.fonte_media = fonte_media
        self.combat_active = True
        self.player_turn = True
        self.result = None
        self.error_message = None
        self.error_start_time = 0
        self.error_duration = 1000
        # Load larger images for combat
        self.player_img = pygame.transform.scale(player.image, (largura // 8, altura // 4))
        self.enemy_img = pygame.transform.scale(enemy.image, (largura // 8, altura // 4))
        self.background = pygame.Surface((largura, altura))
        self.background.fill((50, 50, 50))  # Dark gray background for combat

    def run_combat(self):
        clock = pygame.time.Clock()
        while self.combat_active:
            self.handle_events()
            self.render_combat()
            pygame.display.flip()
            clock.tick(60)
        return self.result

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if self.player_turn:
                    if event.key == pygame.K_1:  # Attack
                        self.player_attack()
                    elif event.key == pygame.K_2:  # Use Boots
                        if self.inventory.has_item("Boots"):
                            self.inventory.use_item("Boots", self.player)
                            self.error_message = None
                        else:
                            self.error_message = "Sem Botas!"
                            self.error_start_time = pygame.time.get_ticks()
                    elif event.key == pygame.K_3:  # Use Umbrella
                        if self.inventory.has_item("Umbrella"):
                            self.inventory.use_item("Umbrella", self.player)
                            self.error_message = None
                        else:
                            self.error_message = "Sem Guarda-chuva!"
                            self.error_start_time = pygame.time.get_ticks()
        if not self.player_turn:
            self.enemy_attack()

    def player_attack(self):
        damage = self.player.damage
        self.enemy.take_damage(damage)
        self.player_turn = False
        if self.enemy.hp <= 0:
            self.combat_active = False
            self.result = "Victory"

    def enemy_attack(self):
        damage = self.enemy.damage
        self.player.take_damage(damage)
        self.player_turn = True
        if self.player.hp <= 0:
            self.combat_active = False
            self.result = "Defeat"

    def render_combat(self):
        tela_combat.blit(self.background, (0, 0))
        # Draw characters
        tela_combat.blit(self.player_img, (largura // 4, altura // 2))
        tela_combat.blit(self.enemy_img, (3 * largura // 4, altura // 2))
        # Draw HP bars
        self.draw_hp_bar(self.player.hp, 100, largura // 4, altura // 2 - 50, "Player")
        self.draw_hp_bar(self.enemy.hp, self.enemy.max_hp, 3 * largura // 4, altura // 2 - 50, "Enemy")
        # Draw action menu horizontally
        if self.player_turn:
            actions = [
                "1 - Atacar",
                f"2 - Usar Bota ({self.inventory.items['Boots']})",
                f"3 - Usar Guarda-chuva ({self.inventory.items['Umbrella']})"
            ]
            total_width = sum(self.fonte_media.size(action)[0] + 40 for action in actions)  # 40px spacing
            x_start = (largura - total_width) // 2  # Center horizontally
            for i, action in enumerate(actions):
                text = self.fonte_media.render(action, True, (255, 255, 255))
                tela_combat.blit(text, (x_start, altura - 100))
                x_start += text.get_width() + 40  # Move right for next action
        # Draw error message if present
        if self.error_message and pygame.time.get_ticks() - self.error_start_time < self.error_duration:
            error_text = self.fonte_media.render(self.error_message, True, (255, 0, 0))
            tela_combat.blit(error_text, (largura // 2 - error_text.get_width() // 2, altura - 50))
        # Draw combat result
        if not self.combat_active:
            result_text = self.fonte_grande.render(self.result, True, (255, 255, 255))
            tela_combat.blit(result_text, (largura // 2 - result_text.get_width() // 2, altura // 2))

    def draw_hp_bar(self, current_hp, max_hp, x, y, label):
        bar_width = 100
        bar_height = 20
        fill = (current_hp / max_hp) * bar_width
        pygame.draw.rect(tela_combat, (255, 0, 0), (x, y, bar_width, bar_height))  # Background
        pygame.draw.rect(tela_combat, (0, 255, 0), (x, y, fill, bar_height))  # Health
        hp_text = self.fonte_media.render(f"{label}: {current_hp}/{max_hp}", True, (255, 255, 255))
        tela_combat.blit(hp_text, (x, y - 30))