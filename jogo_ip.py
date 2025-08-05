import pygame
import sys

ultimo_x = 0

pygame.init()

# Tamanho da tela
largura, altura = 1080, 960
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Mudança de cenário")

# Cenarios
caminhos_fundos = ["entrada_ufpe_2.png", "biblio.jpg", "ru.jpg"]
cenarios = []
for caminho in caminhos_fundos:
    imagem = pygame.image.load(caminho)
    imagem = pygame.transform.scale(imagem, (largura, altura))
    cenarios.append(imagem)

#Carregando personagem
personagem_img = pygame.image.load("kakashi.png")
personagem_img = pygame.transform.scale(personagem_img, (100, 100))

indice_cenario = 0  # Começa no primeiro cenário

# Cor do jogador
cor_jogador = (200, 50, 50)

# Jogador
jogador_tamanho = 50
jogador_x = largura - 100 
jogador_y = altura - 350
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
    if jogador_x <= 0:
        if ultimo_x < 1000:
            #print(f"Valor de do ultimo x foi {ultimo_x}")
            indice_cenario += 1
            jogador_x = largura - jogador_tamanho  # Reposiciona do lado direito

    elif ultimo_x > 1030: # Jogador volta ao cenário anterior
        indice_cenario -= 1
        #print(f"Valor de do ultimo x foi {ultimo_x}")
        jogador_x = 10 # Reposiciona do lado esquerdo
        ultimo_x = 0
    else:
        ultimo_x = jogador_x

    if indice_cenario == 0 and jogador_x > 980:
        jogador_x = 980

    #Limitando o jogador no eixo y
    if jogador_y < 5:
        jogador_y = 5
    if jogador_y > 700:
        jogador_y = 700

    tela.blit(cenarios[indice_cenario], (0, 0))
    tela.blit(personagem_img, (jogador_x, jogador_y))
    pygame.display.flip()
    clock.tick(fps)