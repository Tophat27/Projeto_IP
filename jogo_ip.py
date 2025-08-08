import pygame
import sys
import random
from variaveis import *
from tela import *
from coleta import *



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

        tela.blit(texto, (largura // 2 - 150, 100))
        tela.blit(texto_nome, (largura // 2 - 300, 300))
        tela.blit(texto_esc, (largura // 2 - 250, 500))

        pygame.display.flip()
                

def iniciar_jogo():

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

    # Jogador
    jogador_tamanho = 50
    jogador_x = largura - 200
    jogador_y = altura
    velocidade = 10

    clock = pygame.time.Clock()
    fps = 60


    # Loop principal
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

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

        # Limita posição do jogador para não sair da tela
        if jogador_x < 0:
            jogador_x = 0
        if jogador_x > largura - jogador_tamanho:
            jogador_x = largura - jogador_tamanho

        if indice_cenario == 0 and jogador_x > largura:
            jogador_x = largura

        #Limitando o jogador no eixo y
        if jogador_y < 5:
            jogador_y = 5
        if jogador_y > altura - 280:
            jogador_y = altura - 280

        tela.blit(cenarios[indice_cenario], (0, 0))         #Desenha cenario    
        tela.blit(personagem_img, (jogador_x, jogador_y))   #Desenha personagem
        
        # Posição base (canto inferior esquerdo)
        pos_x = 20
        pos_y = altura - 64 - 20  # 20px de margem inferior

        # Desenha 3 slots lado a lado
        for i in range(3):
            tela.blit(slot_img, (pos_x + i * (128 + 10), altura - 100))

        c1, c2, bota_visivel, guarda_chuva_visivel = coletaveis(indice_cenario, ultimo_cenario, jogador_x, jogador_y, personagem_img, bota_visivel, guarda_chuva_visivel, cont_botas,cont_guarda_chuvas )
        
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