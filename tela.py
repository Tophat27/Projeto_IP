import pygame
from variaveis import *


pygame.init()

largura, altura = get_size()

def tela():
    # Calcular posição para centralizar a janela
    largura_tela = largura - (largura/20)
    altura_tela = altura - (altura/20)
    
    # Centralizar a janela na tela
    pos_x = (largura - largura_tela) // 2
    pos_y = (altura - altura_tela) // 2
    
    # Criar a janela
    # tela = pygame.display.set_mode((int(largura_tela), int(altura_tela)))

    tela = pygame.display.set_mode((largura- (largura/15), altura - (altura/15)))
    pygame.display.set_caption("Game UFPE_Alagada")
    
    # Definir a posição da janela (funciona em alguns sistemas)
    try:
        import os
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{pos_x},{pos_y}"
    except:
        pass
    
    return tela
