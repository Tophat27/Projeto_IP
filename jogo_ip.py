import pygame
import sys
import math

ultimo_x = 0

pygame.init()

# Tamanho da tela
largura, altura = 1080, 960
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Mudança de cenário")

# Cenarios
caminhos_fundos = ["entrada_ufpe.webp", "biblio.jpg", "ru.jpg"]
cenarios = []
for caminho in caminhos_fundos:
    imagem = pygame.image.load(caminho)
    imagem = pygame.transform.scale(imagem, (largura, altura))
    cenarios.append(imagem)

# Carregar sprite da parte de baixo
sprite_baixo = pygame.image.load("Sprite-0001.png")
# Redimensionar o sprite para um tamanho adequado (ajuste conforme necessário)
sprite_baixo = pygame.transform.scale(sprite_baixo, (largura, 300))
# Posição do sprite na parte de baixo da tela (centralizado horizontalmente)
sprite_x = (largura - sprite_baixo.get_width()) // 2
sprite_y = altura - sprite_baixo.get_height() - 20  # 20 pixels de margem do fundo

indice_cenario = 0  # Começa no primeiro cenário

pygame.display.set_caption("Mostrar Variável")
fonte = pygame.font.SysFont("arial", 32)  # Fonte do sistema, tamanho 32

# Cor do jogador
cor_jogador = (200, 50, 50)
cor_inimigo = (50, 50, 200)  # Azul
cor_texto = (255, 255, 255)

# Jogador
jogador_tamanho = 50
jogador_x = largura - 100 
jogador_y = altura - 350
velocidade = 10

# Inimigo
inimigo_tamanho = 40
inimigo_x = 100
inimigo_y = altura - 400
velocidade_inimigo = 3

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

    # Lógica do inimigo perseguindo o jogador
    # Calcular direção do jogador
    dx = jogador_x - inimigo_x
    dy = jogador_y - inimigo_y
    
    # Normalizar o vetor de direção
    distancia = math.sqrt(dx * dx + dy * dy)
    if distancia > 0:
        dx = dx / distancia
        dy = dy / distancia
        
        # Mover o inimigo na direção do jogador
        inimigo_x += dx * velocidade_inimigo
        inimigo_y += dy * velocidade_inimigo

    texto = fonte.render(f"Contador: {jogador_x}", True, cor_texto)
    tela.blit(texto, (0, 0))  # Posição (x, y) do texto na tela
    print(jogador_x)

    # Quando o jogador chega no canto esquerdo da tela, troca de cenário
    if jogador_x <= 0:
        if ultimo_x < 1000:
            # print(f"Valor de do ultimo x foi {ultimo_x}")
            indice_cenario += 1
            jogador_x = largura - jogador_tamanho  # Reposiciona do lado direito

    elif ultimo_x > 1030: # Jogador volta ao cenário anterior
        indice_cenario -= 1
        # print(f"Valor de do ultimo x foi {ultimo_x}")
        jogador_x = 10 # Reposiciona do lado esquerdo
        ultimo_x = 0
    else:
        ultimo_x = jogador_x

    tela.blit(cenarios[indice_cenario], (0, 0))
    # Desenhar o sprite na parte de baixo da tela (entre fundo e jogador)
    tela.blit(sprite_baixo, (sprite_x, sprite_y))
    pygame.draw.rect(tela, cor_jogador, (jogador_x, jogador_y, jogador_tamanho, jogador_tamanho))
    # Desenhar o inimigo
    pygame.draw.rect(tela, cor_inimigo, (inimigo_x, inimigo_y, inimigo_tamanho, inimigo_tamanho))
    pygame.display.flip()
    clock.tick(fps)
