import pygame
import sys
import random
from variaveis import *
from tela import *
from coleta import *

# ============ FUNÇÕES DE DEBUG E MELHORIAS ============

def desenhar_rects_debug(tela_surface, jogador_rect, limites_rect):
    """Desenha retângulos de debug"""
    pygame.draw.rect(tela_surface, (255, 0, 0), jogador_rect, 2)  # Vermelho para o jogador
    pygame.draw.rect(tela_surface, (255, 255, 255), limites_rect, 1)  # Branco para os limites

def desenhar_chao(tela_surface, chao_sprite, largura_tela, altura_tela):
    """Desenha o chão redimensionando a imagem para cobrir 1/3 da tela de baixo para cima"""
    if chao_sprite:
        altura_chao_total = altura_tela // 3  # 1/3 da tela
        posicao_y_inicial = altura_tela - altura_chao_total  # Começa a 1/3 de baixo
        
        # Redimensiona a imagem do chão para cobrir toda a área necessária
        chao_redimensionado = pygame.transform.scale(chao_sprite, (largura_tela, altura_chao_total))
        
        # Desenha o chão redimensionado
        tela_surface.blit(chao_redimensionado, (0, posicao_y_inicial))

def desenhar_rects_colisao(tela_surface, bota_rect, guarda_chuva_rect, bota_visivel, guarda_chuva_visivel):
    """Desenha os retângulos de colisão dos itens"""
    if bota_visivel and bota_rect:
        pygame.draw.rect(tela_surface, (0, 255, 0), bota_rect, 2)  # Verde para bota
    if guarda_chuva_visivel and guarda_chuva_rect:
        pygame.draw.rect(tela_surface, (0, 0, 255), guarda_chuva_rect, 2)  # Azul para guarda-chuva

def aplicar_limites_movimento(jogador_x, jogador_y, personagem_img, largura_tela, altura_tela, altura_chao=280):
    """Aplica os limites de movimento do jogador"""
    jogador_rect = pygame.Rect(jogador_x, jogador_y, personagem_img.get_width(), personagem_img.get_height())
    
    # Define os limites de movimento do jogador (dentro do 1/3 inferior da tela)
    limite_x_min = 0
    limite_x_max = largura_tela - personagem_img.get_width()
    area_movimento = altura_tela // 3  # 1/3 da tela
    limite_y_min = altura_tela - area_movimento  # Começa a 1/3 de baixo
    limite_y_max = altura_tela - personagem_img.get_height()  # Até a parte inferior
    
    # Garante que os limites sejam válidos
    if limite_y_max < limite_y_min:
        limite_y_max = limite_y_min + 100  # Área mínima de movimento
    
    # Cria retângulo de movimento do jogador
    largura_limites = max(0, limite_x_max - limite_x_min)
    altura_limites = max(0, limite_y_max - limite_y_min)
    limites_jogador_rect = pygame.Rect(limite_x_min, limite_y_min, largura_limites, altura_limites)
    
    # Só aplica clamp se o retângulo for válido
    if largura_limites > 0 and altura_limites > 0:
        jogador_rect.clamp_ip(limites_jogador_rect)
    
    # Cria retângulo de debug (caixa branca) que vai de esquerda à direita
    # e cobre 1/3 da tela de baixo para cima
    debug_altura = altura_tela // 3  # 1/3 da tela
    debug_y_start = altura_tela - debug_altura  # Começa a 1/3 de baixo
    limites_debug_rect = pygame.Rect(0, debug_y_start, largura_tela, debug_altura)
    
    return jogador_rect.x, jogador_rect.y, limites_debug_rect

def obter_rect_colisao(jogador_x, jogador_y, personagem_img):
    """Retorna o retângulo de colisão do jogador"""
    return pygame.Rect(jogador_x, jogador_y, personagem_img.get_width(), personagem_img.get_height())

def verificar_colisoes_melhoradas(jogador_rect, bota_rect, guarda_chuva_rect, bota_visivel, guarda_chuva_visivel, cont_botas, cont_guarda_chuvas):
    """Verifica colisões entre o jogador e os itens com retorno de valores"""
    nova_bota_visivel = bota_visivel
    nova_guarda_chuva_visivel = guarda_chuva_visivel
    novo_cont_botas = cont_botas
    novo_cont_guarda_chuvas = cont_guarda_chuvas
    
    if bota_rect and jogador_rect.colliderect(bota_rect) and bota_visivel:
        novo_cont_botas += 1
        nova_bota_visivel = False
    
    if guarda_chuva_rect and jogador_rect.colliderect(guarda_chuva_rect) and guarda_chuva_visivel:
        novo_cont_guarda_chuvas += 1
        nova_guarda_chuva_visivel = False
    
    return novo_cont_botas, novo_cont_guarda_chuvas, nova_bota_visivel, nova_guarda_chuva_visivel

# ============ FIM DAS FUNÇÕES DE DEBUG E MELHORIAS ============

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

# Carregando slot de inventario
slot_img = pygame.image.load("images/slot_inventario.png")
slot_img = pygame.transform.scale(slot_img, (largura // 10, altura // 10))

# Carregando sprite de chão (opcional - se existir)
try:
    chao_sprite = pygame.image.load("images/chao_sprite.png")
    chao_sprite = pygame.transform.scale(chao_sprite, (64, 64))  # Tamanho padrão do tile
except:
    chao_sprite = None  # Se não existir, não usa

# Variáveis de controle para debug
debug_mode = False  # Pressione 'D' para ativar/desativar
mostrar_colisoes = False  # Pressione 'C' para ativar/desativar

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

    # Atualiza e desenha as gotas
    for gota in chuva:
        x, y, comp, vel = gota
        pygame.draw.line(tela, (138, 138, 255), (x, y), (x, y + comp), 1)
        gota[1] += vel

            # Se a gota sair da tela, reinicia no topo
        if gota[1] > altura:
            gota[0] = random.randint(0, largura)
            gota[1] = random.randint(-20, -5)
            gota[3] = random.randint(4, 10)


def desenhar_botao(img_buttom, x, y, acao=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    largura_buttom = img_buttom.get_width()
    altura_buttom = img_buttom.get_height()

    #Verifica se mouse está sobre o botão
    if x < mouse[0] < x + largura_buttom and y < mouse[1] < y + altura_buttom:
        botao_ampliado = pygame.transform.scale(img_buttom, (int(largura_buttom * 1.05), int(altura_buttom * 1.05)))
        tela.blit(botao_ampliado, (x - 5, y - 5))  # desenha botão maior, centralizado
        
        if click[0] == 1 and acao is not None:
            pygame.time.delay(200)  # evita clique duplo
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
        
        # Instruções de controle
        controles = [
            "Controles do Jogo:",
            "Setas - Movimentar personagem",
            "D - Ativar/Desativar modo debug",
            "C - Mostrar/Ocultar colisões",
            "",
            "Recursos Adicionados:",
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
                
            if linha:  # Só renderiza se não for linha vazia
                texto_linha = fonte_usar.render(linha, True, cor)
                tela.blit(texto_linha, (largura // 2 - texto_linha.get_width() // 2, y_pos))
            y_pos += 35
        
        tela.blit(texto_esc, (largura // 2 - 250, y_pos + 50))

        pygame.display.flip()
                

def iniciar_jogo():
    global debug_mode, mostrar_colisoes  # Declarar variáveis globais

    ultimo_x = 0
    ultimo_cenario = 0
    bota_visivel = True
    guarda_chuva_visivel = True
    cont_botas,cont_guarda_chuvas = 0,0

    # Cenarios
    caminhos_fundos = ["images/entrada_ufpe.png", "images/bib_central.png", "images/ru.png", "images/CIn.png"]
    cenarios = []
    for caminho in caminhos_fundos:
        imagem = pygame.image.load(caminho)
        imagem = pygame.transform.scale(imagem, (largura, altura))
        cenarios.append(imagem)

    #Carregando personagem
    personagem_original = pygame.image.load("images/kakashi.png")
    personagem_original = pygame.transform.scale(personagem_original, (largura // 16, altura // 8))
    personagem_espelhado = pygame.transform.flip(personagem_original, True, False)

    personagem_img = personagem_original  # Começa olhando para a esquerda
    olhando_direita = False

    indice_cenario = 0  # Começa no primeiro cenário

    # Jogador - posição inicial no canto inferior direito da área de movimento (1/3 da tela)
    jogador_tamanho = 50
    area_movimento_inicial = altura // 3  # 1/3 da tela
    
    # Canto inferior direito da área de movimento
    jogador_x = largura - personagem_original.get_width() - 5  # Ponta direita com pequena margem
    jogador_y = altura - personagem_original.get_height() - 5  # Parte inferior da área de movimento
    
    velocidade = 10

    clock = pygame.time.Clock()
    fps = 60


    # Loop principal
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_d:
                    debug_mode = not debug_mode  # Toggle debug mode
                elif evento.key == pygame.K_c:
                    mostrar_colisoes = not mostrar_colisoes  # Toggle collision visualization

        # Teclas
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            jogador_x -= velocidade
            if olhando_direita == True:
                personagem_img = personagem_original
                olhando_direita = False
        if teclas[pygame.K_RIGHT]:
            jogador_x += velocidade
            if olhando_direita == False:
                personagem_img = personagem_espelhado
                olhando_direita = True
        if teclas[pygame.K_UP]:
            jogador_y -= velocidade
        if teclas[pygame.K_DOWN]:
            jogador_y += velocidade

        # Quando o jogador chega no canto esquerdo da tela, troca de cenário
        if jogador_x < 0 and indice_cenario < len(cenarios) - 1:
            indice_cenario += 1
            jogador_x = largura - jogador_tamanho  # Reaparece na direita

        # Volta para o cenário anterior (indo para a direita)
        elif jogador_x > largura - jogador_tamanho and indice_cenario > 0:
            indice_cenario -= 1
            jogador_x = 0  # Reaparece na esquerda

        # Aplica os novos limites de movimento melhorados (1/3 da tela para área de movimento)
        altura_chao = altura // 3  # Mantido para compatibilidade
        jogador_x, jogador_y, limites_rect = aplicar_limites_movimento(
            jogador_x, jogador_y, personagem_img, largura, altura, altura_chao
        )
        
        # Limites adicionais para mudança de cenário
        if jogador_x < 0:
            jogador_x = 0
        if jogador_x > largura - jogador_tamanho:
            jogador_x = largura - jogador_tamanho

        if indice_cenario == 0 and jogador_x > largura:
            jogador_x = largura

        tela.blit(cenarios[indice_cenario], (0, 0))         #Desenha cenario    
        
        # Desenha chão se o sprite existir (1/3 da tela de baixo para cima)
        if chao_sprite:
            desenhar_chao(tela, chao_sprite, largura, altura)
        
        tela.blit(personagem_img, (jogador_x, jogador_y))   #Desenha personagem
        
        # Posição base (canto inferior esquerdo)
        pos_x = 20
        pos_y = altura - 64 - 20  # 20px de margem inferior

        # Desenha 3 slots lado a lado
        for i in range(3):
            tela.blit(slot_img, (pos_x + i * (128 + 10), altura - 100))

        # Sistema de coletáveis original (mantido para compatibilidade)
        c1, c2, bota_visivel, guarda_chuva_visivel = coletaveis(indice_cenario, ultimo_cenario, jogador_x, jogador_y, personagem_img, bota_visivel, guarda_chuva_visivel, cont_botas, cont_guarda_chuvas)
        
        # Obtém retângulos de colisão para debug e melhor detecção
        jogador_rect = obter_rect_colisao(jogador_x, jogador_y, personagem_img)
        
        # Tenta obter posições dos itens do módulo coleta para visualização
        bota_rect = None
        guarda_chuva_rect = None
        try:
            # Posições hardcoded baseadas no coleta.py para cada cenário
            if indice_cenario == 0:
                bota_pos = (150, 610)
                guarda_chuva_pos = (450, 610)
            elif indice_cenario == 1:
                bota_pos = (800, 610)
                guarda_chuva_pos = (150, 610)
            elif indice_cenario == 2:
                bota_pos = (300, 610)
                guarda_chuva_pos = (200, 610)
            else:
                bota_pos = None
                guarda_chuva_pos = None
                
            if bota_pos and bota_visivel:
                from coleta import bota_img
                bota_rect = pygame.Rect(bota_pos[0], bota_pos[1], bota_img.get_width(), bota_img.get_height())
            if guarda_chuva_pos and guarda_chuva_visivel:
                from coleta import guarda_chuva_img
                guarda_chuva_rect = pygame.Rect(guarda_chuva_pos[0], guarda_chuva_pos[1], guarda_chuva_img.get_width(), guarda_chuva_img.get_height())
        except:
            pass  # Se houver erro na importação, ignora
        
        # Funções de debug visual
        if debug_mode:
            desenhar_rects_debug(tela, jogador_rect, limites_rect)
            
        if mostrar_colisoes:
            desenhar_rects_colisao(tela, bota_rect, guarda_chuva_rect, bota_visivel, guarda_chuva_visivel)
        
        # Atualiza e desenha as gotas de chuva
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

        # Atualiza e desenha as gotas
        desenhar_chuva()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()

# Inicia o menu
menu_principal()