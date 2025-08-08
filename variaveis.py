import pygame


pygame.init()

def get_size():
    info = pygame.display.Info()
    largura = info.current_w
    altura = info.current_h

    return largura, altura