import pygame
import sys
import random
from variaveis import *
from tela import *
from coleta import *
from enemy import Enemy
from combat import CombatSystem
from inventory import Inventory
from PIL import Image

# ============ PLAYER CLASS ============
class Player:
    def __init__(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.max_hp = 100
        self.hp = 100
        self.damage = 10
        self.looking_right = False

    def take_damage(self, damage):
        self.hp = max(0, self.hp - damage)

    def move(self, dx, dy, velocidade, largura_tela, altura_tela):
        self.rect.x += dx * velocidade
        self.rect.y += dy * velocidade
        # Apply movement limits (1/3 of screen from bottom)
        area_movimento = altura_tela // 3
        limite_y_min = altura_tela - area_movimento
        limite_y_max = altura_tela - self.image.get_height()
        limite_x_min = 0
        limite_x_max = largura_tela - self.image.get_width()
        self.rect.clamp_ip(pygame.Rect(limite_x_min, limite_y_min, limite_x_max - limite_x_min, limite_y_max - limite_y_min))

# ============ FUNÇÕES DE DEBUG E MELHORIAS ============

def desenhar_rects_debug(tela_surface, player_rect, limites_rect):
    """Desenha retângulos de debug"""
    pygame.draw.rect(tela_surface, (255, 0, 0), player_rect, 2)  # Vermelho para o jogador
    pygame.draw.rect(tela_surface, (255, 255, 255), limites_rect, 1)  # Branco para os limites

def desenhar_chao(tela_surface, chao_sprite, largura_tela, altura_tela):
    """Desenha o chão animado com GIF redimensionado para cobrir 1/3 da tela de baixo para cima com 50% de opacidade"""
    global chao_frame_index, chao_last_update
    if chao_sprite:
        altura_chao_total = altura_tela // 4  # 1/3 da tela
        posicao_y_inicial = altura_tela - altura_chao_total  # Começa a 1/3 de baixo
        
        # Update animation frame
        current_time = pygame.time.get_ticks()
        if current_time - chao_last_update > chao_frame_delay:
            chao_frame_index = (chao_frame_index + 1) % len(chao_sprite)  # Cycle through frames
            chao_last_update = current_time
        
        # Redimensiona a imagem do frame atual
        chao_redimensionado = pygame.transform.scale(chao_sprite[chao_frame_index], (largura_tela, altura_chao_total))
        
        # Apply 50% opacity
        chao_redimensionado.set_alpha(127)
        
        # Desenha o frame atual
        tela_surface.blit(chao_redimensionado, (0, posicao_y_inicial))

def desenhar_rects_colisao(tela_surface, bota_rect, guarda_chuva_rect, bota_visivel, guarda_chuva_visivel, enemy):
    """Desenha os retângulos de colisão dos itens e inimigo"""
    if bota_visivel and bota_rect:
        pygame.draw.rect(tela_surface, (0, 255, 0), bota_rect, 2)  # Verde para bota
    if guarda_chuva_visivel and guarda_chuva_rect:
        pygame.draw.rect(tela_surface, (0, 0, 255), guarda_chuva_rect, 2)  # Azul para guarda-chuva
    if enemy:
        pygame.draw.rect(tela_surface, (255, 0, 255), enemy.rect, 2)  # Magenta para inimigo

def aplicar_limites_movimento(player, largura_tela, altura_tela):
    """Aplica os limites de movimento do jogador"""
    area_movimento = altura_tela // 3.5
    limite_y_min = altura_tela - area_movimento
    limite_y_max = altura_tela - player.image.get_height()
    limite_x_min = 0
    limite_x_max = largura_tela - player.image.get_width()
    limites_debug_rect = pygame.Rect(0, limite_y_min, largura_tela, area_movimento)
    return limites_debug_rect

pygame.init()

tela = tela()

# Tela de início (imagem)
imagem_tela_inicio = pygame.image.load("images/tela_inicial.png")
imagem_tela_inicio = pygame.transform.scale(imagem_tela_inicio, (largura, altura))

# Carregando botões
jogar_buttom = pygame.image.load("images/jogar_buttom.png")
jogar_buttom = pygame.transform.scale(jogar_buttom, (largura // 7, altura // 7))

creditos_buttom = pygame.image.load("images/creditos_buttom.png")
creditos_buttom = pygame.transform.scale(creditos_buttom, (largura // 7, altura // 7))

sair_buttom = pygame.image.load("images/sair_buttom.png")
sair_buttom = pygame.transform.scale(sair_buttom, (largura // 7, altura // 7))

# Carregando sprite de chão (opcional - se existir)
try:
    # Load GIF using Pillow
    gif = Image.open("images/agua.gif")
    frames = []
    try:
        while True:
            frame = gif.copy()
            frame = frame.convert("RGBA")  # Ensure RGBA for transparency
            frame_data = frame.tobytes()
            frame_size = frame.size
            pygame_frame = pygame.image.fromstring(frame_data, frame_size, "RGBA")
            frames.append(pygame_frame)
            gif.seek(gif.tell() + 1)  # Next frame
    except EOFError:
        pass  # End of GIF frames
    chao_sprite = frames  # List of frames for animation
    chao_frame_index = 0  # Current frame index
    chao_frame_delay = 100  # Milliseconds per frame (adjust for animation speed)
    chao_last_update = pygame.time.get_ticks()
except:
    chao_sprite = None  # Fallback if GIF fails to load

# Variáveis de controle para debug
debug_mode = False
mostrar_colisoes = False

# Fontes e cores
fonte_grande = pygame.font.SysFont("Arial", 70)
fonte_media = pygame.font.SysFont("Arial", 50)
branco = (255, 255, 255)
cinza = (150, 150, 150)
azul_claro = (100, 200, 255)

# Criar lista de gotas
num_gotas = 200
chuva = []
for _ in range(num_gotas):
    x = random.randint(0, largura)
    y = random.randint(0, altura)
    comprimento = random.randint(5, 15)
    velocidade = random.randint(4, 10)
    chuva.append([x, y, comprimento, velocidade])

def desenhar_chuva():
    for gota in chuva:
        x, y, comp, vel = gota
        pygame.draw.line(tela, (138, 138, 255), (x, y), (x, y + comp), 1)
        gota[1] += vel
        if gota[1] > altura:
            gota[0] = random.randint(0, largura)
            gota[1] = random.randint(-20, -5)
            gota[3] = random.randint(4, 10)

def desenhar_botao(img_buttom, x, y, acao=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    largura_buttom = img_buttom.get_width()
    altura_buttom = img_buttom.get_height()
    if x < mouse[0] < x + largura_buttom and y < mouse[1] < y + altura_buttom:
        botao_ampliado = pygame.transform.scale(img_buttom, (int(largura_buttom * 1.05), int(altura_buttom * 1.05)))
        tela.blit(botao_ampliado, (x - 5, y - 5))
        if click[0] == 1 and acao is not None:
            pygame.time.delay(200)
            acao()
    else:
        tela.blit(img_buttom, (x, y))

def mostrar_creditos():
    mostrando = True
    fonte_pequena = pygame.font.SysFont("Arial", 30)
    while mostrando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                mostrando = False
        tela.fill((0, 0, 0))
        texto = fonte_grande.render("Créditos", True, branco)
        texto_nome = fonte_media.render("Desenvolvido por Pedro (phhs)", True, branco)
        texto_esc = fonte_media.render("Pressione ESC para voltar", True, branco)
        controles = [
            "Controles do Jogo:",
            "Setas - Movimentar personagem",
            "D - Ativar/Desativar modo debug",
            "C - Mostrar/Ocultar colisões",
            "1 - Atacar (em combate)",
            "2 - Usar Botas (em combate, se disponível)",
            "3 - Usar Guarda-chuva (em combate, se disponível)",
            "",
            "Recursos Adicionados:",
            "• Sistema de combate por turnos",
            "• Sistema de inventário",
            "• Inimigos com spawn dinâmico",
            "• Sistema de debug visual",
            "• Visualização de colisões",
            "• Limites de movimento melhorados",
            "• Suporte para sprite de chão"
        ]
        tela.blit(texto, (largura // 2 - 150, 50))
        tela.blit(texto_nome, (largura // 2 - 300, 150))
        y_pos = 250
        for linha in controles:
            if linha == "Controles do Jogo:" or linha == "Recursos Adicionados:":
                cor = azul_claro
                fonte_usar = fonte_media
            elif linha.startswith("•"):
                cor = cinza
                fonte_usar = fonte_pequena
            else:
                cor = branco
                fonte_usar = fonte_pequena
            if linha:
                texto_linha = fonte_usar.render(linha, True, cor)
                tela.blit(texto_linha, (largura // 2 - texto_linha.get_width() // 2, y_pos))
            y_pos += 35
        tela.blit(texto_esc, (largura // 2 - 250, y_pos + 50))
        pygame.display.flip()

def iniciar_jogo():
    global debug_mode, mostrar_colisoes
    bota_visivel = True
    guarda_chuva_visivel = True
    ultimo_cenario = 0
    # Initialize inventory
    inventory = Inventory()
    # Cenarios
    caminhos_fundos = ["images/entrada_ufpe.png", "images/bib_central.png", "images/ru.png", "images/CIn.png"]
    cenarios = []
    for caminho in caminhos_fundos:
        imagem = pygame.image.load(caminho)
        imagem = pygame.transform.scale(imagem, (largura, altura))
        cenarios.append(imagem)
    # Carregando personagem
    personagem_original = pygame.image.load("images/kakashi.png")
    personagem_original = pygame.transform.scale(personagem_original, (largura // 16, altura // 8))
    personagem_espelhado = pygame.transform.flip(personagem_original, True, False)
    # Initialize player
    player = Player(personagem_original, largura - personagem_original.get_width() - 5, altura - personagem_original.get_height() - 5)
    velocidade = 10
    clock = pygame.time.Clock()
    fps = 60
    indice_cenario = 0
    enemy = None  # No enemy at start
    spawn_delay = 1000  # 1-second delay before enemy can spawn (in milliseconds)
    last_spawn_time = pygame.time.get_ticks()
    enemy_defeated_in_scenario = {i: False for i in range(len(cenarios))}  # Track defeated enemies per scenario
    # Loop principal
    while True:
        current_time = pygame.time.get_ticks()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_d:
                    debug_mode = not debug_mode
                elif evento.key == pygame.K_c:
                    mostrar_colisoes = not mostrar_colisoes
        # Handle movement
        dx, dy = 0, 0
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            dx = -1
            if player.looking_right:
                player.image = personagem_original
                player.looking_right = False
        if teclas[pygame.K_RIGHT]:
            dx = 1
            if not player.looking_right:
                player.image = personagem_espelhado
                player.looking_right = True
        if teclas[pygame.K_UP]:
            dy = -1
        if teclas[pygame.K_DOWN]:
            dy = 1
        player.move(dx, dy, velocidade, largura, altura)
        # Spawn enemy only after delay, if player moves leftward, and if not defeated in this scenario
        if not enemy and not enemy_defeated_in_scenario[indice_cenario] and current_time - last_spawn_time > spawn_delay and player.rect.x < largura - 100:
            enemy = Enemy()
            last_spawn_time = current_time
        # Move enemy to match player's y-position
        if enemy:
            enemy.move(player.rect.y)
        # Check for combat trigger
        combat_triggered = False
        if enemy and current_time - last_spawn_time > spawn_delay and (player.rect.colliderect(enemy.rect) or abs(player.rect.x - enemy.rect.x) < 10):
            combat_system = CombatSystem(player, enemy, inventory, fonte_grande, fonte_media)
            result = combat_system.run_combat()
            if result == "Victory":
                enemy = None  # Remove enemy
                enemy_defeated_in_scenario[indice_cenario] = True  # Mark enemy as defeated in this scenario
                last_spawn_time = current_time  # Reset spawn delay
            elif result == "Defeat":
                pygame.quit()
                sys.exit()  # Game over
            combat_triggered = True
        # Scenario change logic (moved outside combat_triggered block)
        if player.rect.x < 0 and indice_cenario < len(cenarios) - 1:
            indice_cenario += 1
            player.rect.x = largura - player.image.get_width()
            enemy = None  # Reset enemy
            enemy_defeated_in_scenario[indice_cenario] = False  # Allow new enemy in new scenario
            last_spawn_time = current_time
        elif player.rect.x > largura - player.image.get_width() and indice_cenario > 0:
            indice_cenario -= 1
            player.rect.x = 0
            enemy = None  # Reset enemy
            enemy_defeated_in_scenario[indice_cenario] = False  # Allow new enemy in new scenario
            last_spawn_time = current_time
        # Draw scenario
        tela.blit(cenarios[indice_cenario], (0, 0))
        if chao_sprite:
            desenhar_chao(tela, chao_sprite, largura, altura)
        # Draw player and enemy
        tela.blit(player.image, player.rect.topleft)
        if enemy:
            tela.blit(enemy.image, enemy.rect.topleft)
        # Draw collectibles
        bota_rect, guarda_chuva_rect, bota_visivel, guarda_chuva_visivel = coletaveis(indice_cenario, ultimo_cenario, player.rect.x, player.rect.y, player.image, bota_visivel, guarda_chuva_visivel, inventory)
        # Draw inventory
        inventory.draw(tela)
        # Debug and collision visuals
        limites_rect = aplicar_limites_movimento(player, largura, altura)
        if debug_mode:
            desenhar_rects_debug(tela, player.rect, limites_rect)
        if mostrar_colisoes:
            desenhar_rects_colisao(tela, bota_rect, guarda_chuva_rect, bota_visivel, guarda_chuva_visivel, enemy)
        # Update rain
        desenhar_chuva()
        ultimo_cenario = indice_cenario
        pygame.display.flip()
        clock.tick(fps)


# Tela de menu principal
def menu_principal():
    while True:
        tela.blit(imagem_tela_inicio, (0, 0))
        desenhar_botao(jogar_buttom, largura // 2 - 150, altura // 2 - 100, iniciar_jogo)
        desenhar_botao(creditos_buttom, largura // 2 - 150, altura // 2 + 0, mostrar_creditos)
        desenhar_botao(sair_buttom, largura // 2 - 150, altura // 2 + 100, pygame.quit)
        desenhar_chuva()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.flip()

menu_principal()