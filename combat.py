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
    def __init__(self, player, enemy, inventory, fonte_grande, fonte_media, background):
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
        self.error_duration = 1000  # 1 segundo em milissegundos
        self.used_item_this_round = False  # Rastrear uso de item no turno
        # Carregar imagens maiores para combate
        self.player_img = pygame.transform.scale(player.image, (largura // 8, altura // 4))
        self.enemy_img = pygame.transform.scale(enemy.image, (largura // 8, altura // 4))
        # Carregar fundo principal
        try:
            self.background = pygame.image.load(f"{background}")
            self.background = pygame.transform.scale(self.background, (largura, altura))
        except:
            # Fallback para fundo cinza se a imagem não for encontrada
            self.background = pygame.Surface((largura, altura))
            self.background.fill((50, 50, 50))  # Cinza escuro
        # Carregar imagem da plataforma para personagens
        try:
            self.platform = pygame.image.load("images/character_platform.png")
            self.platform = pygame.transform.scale(self.platform, (largura // 3, altura // 4))
        except:
            # Fallback para plataforma cinza se a imagem não for encontrada
            self.platform = pygame.Surface((largura // 8, altura // 8))
            self.platform.fill((100, 100, 100))  # Cinza médio

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
                    if event.key == pygame.K_1:  # Atacar
                        self.player_attack()
                    elif event.key == pygame.K_2:  # Usar Bota
                        if self.used_item_this_round:
                            self.error_message = "Apenas um item por turno!"
                            self.error_start_time = pygame.time.get_ticks()
                        elif self.inventory.has_item("Boots"):
                            self.inventory.use_item("Boots", self.player)
                            self.used_item_this_round = True
                            self.error_message = None
                        else:
                            self.error_message = "Sem Botas!"
                            self.error_start_time = pygame.time.get_ticks()
                    elif event.key == pygame.K_3:  # Usar Guarda-chuva
                        if self.used_item_this_round:
                            self.error_message = "Apenas um item por turno!"
                            self.error_start_time = pygame.time.get_ticks()
                        elif self.inventory.has_item("Umbrella"):
                            self.inventory.use_item("Umbrella", self.player)
                            self.used_item_this_round = True
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
        self.used_item_this_round = False 
        if self.enemy.hp <= 0:
            self.combat_active = False
            self.result = "Victory"

    def enemy_attack(self):
        damage = self.enemy.damage
        self.player.take_damage(damage)
        self.player_turn = True
        self.used_item_this_round = False 
        if self.player.hp <= 0:
            self.combat_active = False
            self.result = "Defeat"

    def render_combat(self):
        # Desenhar fundo principal
        tela_combat.blit(self.background, (0, 0))
        # Desenhar plataformas sob os personagens
        platform_y = altura // 2.2 + self.player_img.get_height() - self.platform.get_height() // 2  # Alinhar com a base dos personagens
        tela_combat.blit(self.platform, (largura // 4 - self.platform.get_width() // 2, platform_y))  # Plataforma do jogador
        tela_combat.blit(self.platform, (3 * largura // 4 - self.platform.get_width() // 2, platform_y))  # Plataforma do inimigo
        # Desenhar personagens
        tela_combat.blit(self.player_img, (largura // 4 - self.player_img.get_width() // 2, altura // 2))
        tela_combat.blit(self.enemy_img, (3 * largura // 4 - self.enemy_img.get_width() // 2, altura // 2))
        # Desenhar barras de HP
        self.draw_hp_bar(self.player.hp, 100, largura // 4, altura // 2 - 50, "Player")
        self.draw_hp_bar(self.enemy.hp, self.enemy.max_hp, 3 * largura // 4, altura // 2 - 50, "Enemy")
        # Desenhar menu de ações horizontalmente
        if self.player_turn:
            actions = [
                "1 - Atacar",
                f"2 - Usar Bota ({self.inventory.items['Boots']})",
                f"3 - Usar Guarda-chuva ({self.inventory.items['Umbrella']})"
            ]
            total_width = sum(self.fonte_media.size(action)[0] + 40 for action in actions)  # 40px de espaçamento
            x_start = (largura - total_width) // 2  # Centralizar horizontalmente
            for i, action in enumerate(actions):
                text = self.fonte_media.render(action, True, (255, 255, 255))
                tela_combat.blit(text, (x_start, altura - 100))
                x_start += text.get_width() + 40  # Mover para a direita
        # Desenhar mensagem de erro se presente
        if self.error_message and pygame.time.get_ticks() - self.error_start_time < self.error_duration:
            error_text = self.fonte_media.render(self.error_message, True, (255, 0, 0))
            tela_combat.blit(error_text, (largura // 2 - error_text.get_width() // 2, altura - 50))
        # Desenhar resultado do combate
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