import pygame
from variaveis import *


pygame.init()

largura, altura = get_size()

def tela():

    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Game UFPE_Alagada")
    return tela
