import pygame
import sys

ultimo_x = 0

pygame.init()

# Detecta resolução da tela do usuário
info = pygame.display.Info()
largura = info.current_w
altura = info.current_h

# Tamanho da tela
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Game UFPE_Alagada")

# Cenarios
caminhos_fundos = ["entrada_ufpe_2.png", "bib_central.png", "ru.jpg"]
cenarios = []
for caminho in caminhos_fundos:
    imagem = pygame.image.load(caminho)
    imagem = pygame.transform.scale(imagem, (largura, altura))
    cenarios.append(imagem)

#Carregando personagem
personagem_img = pygame.image.load("kakashi.png")
personagem_img = pygame.transform.scale(personagem_img, (altura / 10, largura/10))

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
    if teclas[pygame.K_RIGHT]:
        jogador_x += velocidade
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

    tela.blit(cenarios[indice_cenario], (0, 0))
    tela.blit(personagem_img, (jogador_x, jogador_y))
    pygame.display.flip()
    clock.tick(fps)