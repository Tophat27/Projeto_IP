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
from musica_config import inicializar_musica_jogo, tocar_musica_jogo, parar_musica_jogo, inicializar_musica_combate, inicializar_som_ataque, inicializar_som_ataque_inimigo, inicializar_som_vitoria

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
        limite_x_min = -10  # Allow slight negative x to trigger transition
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
pygame.mixer.init()  # Inicializar sistema de áudio

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

# Carregando música de fundo para o menu
try:
    pygame.mixer.music.load("SFX/Time for a Smackdown.mp3")
    pygame.mixer.music.set_volume(0.25)  # Volume em 25%
    print("Música carregada com sucesso")
except Exception as e:
    print(f"Erro ao carregar música: {e}")
    pygame.mixer.music = None

# Carregando música de fundo para o jogo
try:
    inicializar_musica_jogo()
    print("Música do jogo carregada com sucesso")
except Exception as e:
    print(f"Erro ao carregar música do jogo: {e}")

# Carregando música de combate
try:
    inicializar_musica_combate()
    print("Música de combate carregada com sucesso")
except Exception as e:
    print(f"Erro ao carregar música de combate: {e}")

# Carregando som de ataque
try:
    inicializar_som_ataque()
    print("Som de ataque carregado com sucesso")
except Exception as e:
    print(f"Erro ao carregar som de ataque: {e}")

# Carregando som de ataque do inimigo
try:
    inicializar_som_ataque_inimigo()
    print("Som de ataque do inimigo carregado com sucesso")
except Exception as e:
    print(f"Erro ao carregar som de ataque do inimigo: {e}")

# Carregando som de vitória
try:
    inicializar_som_vitoria()
    print("Som de vitória carregado com sucesso")
except Exception as e:
    print(f"Erro ao carregar som de vitória: {e}")

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
    # Parar música do menu
    if pygame.mixer.music:
        pygame.mixer.music.stop()
        print("Música do menu parada")
    
    mostrando = True
    fonte_pequena = pygame.font.SysFont("Arial", 30)
    while mostrando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                mostrando = False
                # Retomar música do menu
                if pygame.mixer.music:
                    pygame.mixer.music.play(-1)
                    print("Música do menu retomada")
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
            "Controles de Áudio:",
            "M - Mutar/Desmutar música",
            "+ - Aumentar volume",
            "- - Diminuir volume",
            "",
            "Recursos Adicionados:",
            "• Sistema de combate por turnos",
            "• Sistema de inventário",
            "• Inimigos com spawn dinâmico",
            "• Sistema de debug visual",
            "• Visualização de colisões",
            "• Limites de movimento melhorados",
            "• Suporte para sprite de chão",
            "• Música de fundo em loop"
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
    # Parar música do menu
    if pygame.mixer.music:
        pygame.mixer.music.stop()
        print("Música do menu parada")
    
    # Iniciar música do jogo em loop
    tocar_musica_jogo()
    
    global debug_mode, mostrar_colisoes
    bota_visivel = True
    guarda_chuva_visivel = True
    cracha_visivel = True
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
    # Carregando sprite de personagem (GIF animado)
    try:
        gif_personagem = Image.open("images/john ip.gif")
        frames_personagem = []
        for frame in range(gif_personagem.n_frames):
            gif_personagem.seek(frame)
            frame_surface = pygame.image.fromstring(gif_personagem.convert("RGBA").tobytes(), gif_personagem.size, "RGBA")
            frame_surface = pygame.transform.scale(frame_surface, (largura // 16, altura // 8))
            frames_personagem.append(frame_surface)
        
        # Criar versões espelhadas para movimento para a esquerda
        frames_personagem_espelhados = []
        for frame in frames_personagem:
            frame_espelhado = pygame.transform.flip(frame, True, False)
            frames_personagem_espelhados.append(frame_espelhado)
        
        personagem_original = frames_personagem[0]
        personagem_espelhado = frames_personagem_espelhados[0]
        personagem_frame_index = 0
        personagem_frame_delay = 150
        personagem_last_update = pygame.time.get_ticks()
        
        # Carregar GIF de caminhada
        gif_caminhada = Image.open("images/John ip Walk.gif")
        frames_caminhada = []
        for frame in range(gif_caminhada.n_frames):
            gif_caminhada.seek(frame)
            frame_surface = pygame.image.fromstring(gif_caminhada.convert("RGBA").tobytes(), gif_caminhada.size, "RGBA")
            frame_surface = pygame.transform.scale(frame_surface, (largura // 16, altura // 8))
            frames_caminhada.append(frame_surface)
        
        # Criar versões espelhadas para caminhada
        frames_caminhada_espelhados = []
        for frame in frames_caminhada:
            frame_espelhado = pygame.transform.flip(frame, True, False)
            frames_caminhada_espelhados.append(frame_espelhado)
        
        caminhada_frame_index = 0
        caminhada_frame_delay = 100  # Mais rápido que o sprite parado
        caminhada_last_update = pygame.time.get_ticks()
        
    except:
        # Fallback para imagem estática
        personagem_original = pygame.image.load("images/john ip.gif")
        personagem_original = pygame.transform.scale(personagem_original, (largura // 16, altura // 8))
        personagem_espelhado = pygame.transform.flip(personagem_original, True, False)
        frames_personagem = None
        frames_caminhada = None
    # Initialize player
    player = Player(personagem_original, largura - personagem_original.get_width() - 5, altura - personagem_original.get_height() - 5)
    if 'frames_personagem' in locals() and frames_personagem:
        player.frames_personagem = frames_personagem
        player.frames_personagem_espelhados = frames_personagem_espelhados
        player.personagem_frame_index = personagem_frame_index
        player.personagem_frame_delay = personagem_frame_delay
        player.personagem_last_update = personagem_last_update
    if 'frames_caminhada' in locals() and frames_caminhada:
        player.frames_caminhada = frames_caminhada
        player.frames_caminhada_espelhados = frames_caminhada_espelhados
        player.caminhada_frame_index = caminhada_frame_index
        player.caminhada_frame_delay = caminhada_frame_delay
        player.caminhada_last_update = caminhada_last_update
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
        
        # Update character animation if using GIF
        if 'frames_personagem' in locals() and frames_personagem:
            current_time = pygame.time.get_ticks()
            
            # Verificar se o jogador está se movendo
            is_moving = any([teclas[pygame.K_LEFT], teclas[pygame.K_RIGHT], teclas[pygame.K_UP], teclas[pygame.K_DOWN]])
            
            if is_moving and hasattr(player, 'frames_caminhada') and player.frames_caminhada:
                # Usar animação de caminhada
                if current_time - player.caminhada_last_update > player.caminhada_frame_delay:
                    player.caminhada_frame_index = (player.caminhada_frame_index + 1) % len(player.frames_caminhada)
                    player.caminhada_last_update = current_time
                    if player.looking_right:
                        player.image = player.frames_caminhada_espelhados[player.caminhada_frame_index]
                    else:
                        player.image = player.frames_caminhada[player.caminhada_frame_index]
            else:
                # Usar animação parada
                if current_time - player.personagem_last_update > player.personagem_frame_delay:
                    player.personagem_frame_index = (player.personagem_frame_index + 1) % len(frames_personagem)
                    player.personagem_last_update = current_time
                    if player.looking_right:
                        player.image = frames_personagem_espelhados[player.personagem_frame_index]
                    else:
                        player.image = frames_personagem[player.personagem_frame_index]
        
        # Debug print to track transition condition
        if debug_mode:
            print(f"Player x: {player.rect.x}, Scenario: {indice_cenario}")
        # Scenario change logic
        if player.rect.x <= -10 and indice_cenario < len(cenarios) - 1:
            indice_cenario += 1
            player.rect.x = largura - player.image.get_width()
            enemy = None
            enemy_defeated_in_scenario[indice_cenario] = False
            last_spawn_time = current_time
            print(f"Transitioned to next scenario: {indice_cenario}")
        elif player.rect.x > largura - player.image.get_width() and indice_cenario > 0:
            indice_cenario -= 1
            player.rect.x = 0
            enemy = None
            enemy_defeated_in_scenario[indice_cenario] = False
            last_spawn_time = current_time
            print(f"Transitioned to previous scenario: {indice_cenario}")
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
            combat_system = CombatSystem(player, enemy, inventory, fonte_grande, fonte_media, caminhos_fundos[indice_cenario])
            result = combat_system.run_combat()
            if result == "Victory":
                enemy = None
                enemy_defeated_in_scenario[indice_cenario] = True
                player.hp = min(player.hp +20, 100)
                last_spawn_time = current_time
            elif result == "Defeat":
                pygame.quit()
                sys.exit()
            combat_triggered = True
        # Draw scenario
        tela.blit(cenarios[indice_cenario], (0, 0))
        if chao_sprite:
            desenhar_chao(tela, chao_sprite, largura, altura)
        # Draw player and enemy
        tela.blit(player.image, player.rect.topleft)
        if enemy:
            tela.blit(enemy.image, enemy.rect.topleft)
        # Draw collectibles
        bota_rect, guarda_chuva_rect, bota_visivel, guarda_chuva_visivel, cracha_visivel = coletaveis(indice_cenario, ultimo_cenario, player.rect.x, player.rect.y, player.image, bota_visivel, guarda_chuva_visivel, inventory, cracha_visivel)
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
    # Iniciar música em loop
    if pygame.mixer.music:
        pygame.mixer.music.play(-1)  # -1 significa loop infinito
        print("Música iniciada em loop")
    
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
            elif evento.type == pygame.KEYDOWN:
                # Controles de volume
                if evento.key == pygame.K_PLUS or evento.key == pygame.K_KP_PLUS:
                    # Aumentar volume
                    if pygame.mixer.music:
                        current_volume = pygame.mixer.music.get_volume()
                        new_volume = min(1.0, current_volume + 0.1)
                        pygame.mixer.music.set_volume(new_volume)
                        print(f"Volume: {int(new_volume * 100)}%")
                elif evento.key == pygame.K_MINUS or evento.key == pygame.K_KP_MINUS:
                    # Diminuir volume
                    if pygame.mixer.music:
                        current_volume = pygame.mixer.music.get_volume()
                        new_volume = max(0.0, current_volume - 0.1)
                        pygame.mixer.music.set_volume(new_volume)
                        print(f"Volume: {int(new_volume * 100)}%")
                elif evento.key == pygame.K_m:
                    # Mutar/desmutar música
                    if pygame.mixer.music:
                        if pygame.mixer.music.get_volume() > 0:
                            pygame.mixer.music.set_volume(0.0)
                            print("Música mutada")
                        else:
                            pygame.mixer.music.set_volume(0.25)
                            print("Música desmutada")
        
        pygame.display.flip()

menu_principal()