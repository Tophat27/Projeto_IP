import pygame
import os

# Inicializa o Pygame
pygame.init()

# Cria uma superfície para o sprite do chão
largura_sprite = 200
altura_sprite = 100
chao_surface = pygame.Surface((largura_sprite, altura_sprite))

# Cores baseadas na descrição da imagem
verde_escuro = (34, 51, 34)
vermelho_escuro = (85, 34, 34)
azul_escuro = (34, 51, 68)
verde_claro = (51, 68, 51)
azul_claro = (51, 68, 85)

# Desenha as listras horizontais (baseado na descrição da imagem)
# Listra 1: Verde escuro com textura
pygame.draw.rect(chao_surface, verde_escuro, (0, 0, largura_sprite, 15))
# Adiciona textura sutil
for x in range(0, largura_sprite, 3):
    pygame.draw.line(chao_surface, verde_claro, (x, 0), (x, 15), 1)

# Listra 2: Vermelho escuro
pygame.draw.rect(chao_surface, vermelho_escuro, (0, 15, largura_sprite, 25))

# Listra 3: Verde escuro
pygame.draw.rect(chao_surface, verde_escuro, (0, 40, largura_sprite, 20))

# Listra 4: Azul escuro
pygame.draw.rect(chao_surface, azul_escuro, (0, 60, largura_sprite, 15))

# Listra 5: Azul escuro com textura
pygame.draw.rect(chao_surface, azul_escuro, (0, 75, largura_sprite, 10))
# Adiciona textura sutil
for x in range(0, largura_sprite, 3):
    pygame.draw.line(chao_surface, azul_claro, (x, 75), (x, 85), 1)

# Listra 6: Verde escuro com textura
pygame.draw.rect(chao_surface, verde_escuro, (0, 85, largura_sprite, 15))
# Adiciona textura sutil
for x in range(0, largura_sprite, 3):
    pygame.draw.line(chao_surface, verde_claro, (x, 85), (x, 100), 1)

# Cria o diretório images se não existir
if not os.path.exists("images"):
    os.makedirs("images")

# Salva a imagem
pygame.image.save(chao_surface, "images/chao_sprite.png")
print("Sprite de chão criado com sucesso em 'images/chao_sprite.png'")

# Opcional: Mostra a imagem criada
tela = pygame.display.set_mode((largura_sprite, altura_sprite))
pygame.display.set_caption("Sprite de Chão - Pressione qualquer tecla para sair")
tela.blit(chao_surface, (0, 0))
pygame.display.flip()

# Aguarda o usuário fechar a janela
aguardando = True
while aguardando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT or evento.type == pygame.KEYDOWN:
            aguardando = False

pygame.quit()

