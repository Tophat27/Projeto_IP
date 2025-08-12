# enemy.py
# Manages enemy spawning and behavior.

import pygame
import random
from variaveis import get_size
from PIL import Image

largura, _ = get_size()

class Enemy:
    def __init__(self, hp=40, enemy_type="default"):
        self.max_hp = hp
        self.hp = hp
        self.enemy_type = enemy_type
        
        # Variáveis para animação
        self.frames = []
        self.frame_index = 0
        self.frame_delay = 150  # Milissegundos por frame
        self.last_update = pygame.time.get_ticks()
        
        # Configurações específicas por tipo de inimigo
        if enemy_type == "entrada":
            # Carregar GIF animado para entrada
            try:
                gif = Image.open("images/inimigo 1.gif")
                self.frames = []
                for frame in range(gif.n_frames):
                    gif.seek(frame)
                    frame_surface = pygame.image.fromstring(gif.convert("RGBA").tobytes(), gif.size, "RGBA")
                    frame_surface = pygame.transform.scale(frame_surface, (largura // 16, largura // 8))
                    self.frames.append(frame_surface)
                self.image = self.frames[0]  # Frame inicial
                print(f"GIF carregado com {len(self.frames)} frames para inimigo entrada")
            except Exception as e:
                print(f"Erro ao carregar GIF: {e}")
                # Fallback para imagem estática
                self.image = pygame.image.load("images/inimigo 1.gif")
                self.image = pygame.transform.scale(self.image, (largura // 16, largura // 8))
                self.frames = []
            
            self.damage = random.randint(3, 15)  # Inimigo mais fraco
            self.hp = 20
            self.max_hp = 20
            
        elif enemy_type == "biblioteca":
            # Carregar GIF animado para biblioteca
            try:
                gif = Image.open("images/clippy-microsoft.gif")
                self.frames = []
                for frame in range(gif.n_frames):
                    gif.seek(frame)
                    frame_surface = pygame.image.fromstring(gif.convert("RGBA").tobytes(), gif.size, "RGBA")
                    frame_surface = pygame.transform.scale(frame_surface, (largura // 16, largura // 8))
                    self.frames.append(frame_surface)
                self.image = self.frames[0]  # Frame inicial
                print(f"GIF carregado com {len(self.frames)} frames para inimigo biblioteca")
            except Exception as e:
                print(f"Erro ao carregar GIF da biblioteca: {e}")
                # Fallback para imagem estática
                try:
                    self.image = pygame.image.load("images/clippy-microsoft.gif")
                    self.image = pygame.transform.scale(self.image, (largura // 16, largura // 8))
                except:
                    # Se falhar, criar um inimigo padrão colorido
                    self.image = pygame.Surface((largura // 16, largura // 8))
                    self.image.fill((0, 255, 0))  # Verde como fallback
                self.frames = []
            
            self.damage = random.randint(7, 20)  # Inimigo médio
            self.hp = 35
            self.max_hp = 35
            
        elif enemy_type == "ru":
            # Carregar GIF animado para RU
            try:
                gif = Image.open("images/crocodile.gif")
                self.frames = []
                for frame in range(gif.n_frames):
                    gif.seek(frame)
                    frame_surface = pygame.image.fromstring(gif.convert("RGBA").tobytes(), gif.size, "RGBA")
                    frame_surface = pygame.transform.scale(frame_surface, (largura // 16, largura // 8))
                    self.frames.append(frame_surface)
                self.image = self.frames[0]  # Frame inicial
                print(f"GIF carregado com {len(self.frames)} frames para inimigo RU")
            except Exception as e:
                print(f"Erro ao carregar GIF do RU: {e}")
                # Fallback para imagem estática
                try:
                    self.image = pygame.image.load("images/crocodile.gif")
                    self.image = pygame.transform.scale(self.image, (largura // 16, largura // 8))
                except:
                    # Se falhar, criar um inimigo padrão colorido
                    self.image = pygame.Surface((largura // 16, largura // 8))
                    self.image.fill((0, 0, 255))  # Azul como fallback
                self.frames = []
            
            self.damage = random.randint(10, 25)  # Inimigo forte
            self.hp = 50
            self.max_hp = 50
            
        elif enemy_type == "cin":
            self.image = pygame.image.load("images/image-removebg-preview.png")
            self.image = pygame.transform.scale(self.image, (largura // 16, largura // 8))
            self.damage = random.randint(15, 30)  # Boss final
            self.hp = 70
            self.max_hp = 70
            
        else:
            # Fallback para inimigo padrão
            try:
                self.image = pygame.image.load("images/enemy.png")
            except:
                # Se não encontrar enemy.png, criar um inimigo padrão colorido
                self.image = pygame.Surface((largura // 16, largura // 8))
                self.image.fill((255, 0, 0))  # Vermelho como fallback
            self.damage = random.randint(5, 25)
            self.hp = 40
            self.max_hp = 40
            
        self.rect = self.image.get_rect(topleft=(0, 0))

    def take_damage(self, damage):
        self.hp = max(0, self.hp - damage)

    def update_animation(self):
        """Atualiza a animação do inimigo se for um GIF"""
        if self.frames and len(self.frames) > 1:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_update > self.frame_delay:
                self.frame_index = (self.frame_index + 1) % len(self.frames)
                self.image = self.frames[self.frame_index]
                self.last_update = current_time

    def move(self, player_y):
        # Atualizar animação primeiro
        self.update_animation()
        
        # Comportamento diferente por tipo de inimigo
        if self.enemy_type == "cin":
            # Boss mais agressivo - move mais rápido e tem movimento horizontal sutil
            self.rect.y = player_y
            # Adicionar movimento horizontal sutil para parecer mais ameaçador
            self.rect.x += random.randint(-2, 2)
            # Manter o boss dentro dos limites da tela
            self.rect.x = max(0, min(self.rect.x, largura - self.image.get_width()))
        elif self.enemy_type == "ru":
            # Inimigo do RU - movimento mais errático
            self.rect.y = player_y
            # Movimento horizontal mais variado
            if random.random() < 0.1:  # 10% de chance de mudar direção
                self.rect.x += random.randint(-3, 3)
            self.rect.x = max(0, min(self.rect.x, largura - self.image.get_width()))
        elif self.enemy_type == "biblioteca":
            # Inimigo da biblioteca - movimento mais suave
            self.rect.y = player_y
            # Movimento horizontal sutil
            if random.random() < 0.05:  # 5% de chance de mudar direção
                self.rect.x += random.randint(-1, 1)
            self.rect.x = max(0, min(self.rect.x, largura - self.image.get_width()))
        else:
            # Inimigos normais (entrada e padrão) - movimento simples
            self.rect.y = player_y