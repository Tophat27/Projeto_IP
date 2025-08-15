import pygame
from variaveis import get_size
from sys import exit
from tela import *

pygame.init()
caixa = pygame.image.load('images/balao_ip.png').convert_alpha()
caixa = pygame.transform.scale(caixa, (580, 230))
fonte = pygame.font.SysFont('arial', 17, True, False)

mostrar_balao = False
balao_inicio_tempo = 0
balao_duracao = 3000
balao_texto = ""
balao_rect = None

def alocar_texto(tela, texto, caixa_rect):
    texto_rend = fonte.render(texto, True, (0, 0, 0))
    texto_rect = texto_rend.get_rect(center=(caixa_rect.centerx, caixa_rect.centery - 30))
    tela.blit(texto_rend, texto_rect)

def alocar_caixa(tela, player_rect, texto):
    global mostrar_balao, balao_inicio_tempo, balao_texto, balao_rect
    pos_x = player_rect.x - 200
    pos_y = player_rect.y - 190
    balao_rect = caixa.get_rect(topleft=(pos_x, pos_y))
    balao_texto = texto
    mostrar_balao = True
    balao_inicio_tempo = pygame.time.get_ticks()
    tela.blit(caixa, balao_rect)
    alocar_texto(tela, texto, balao_rect)

def atualizar_balao(tela, player_rect):
    global mostrar_balao
    if mostrar_balao:
        pos_x = player_rect.x - 200
        pos_y = player_rect.y - 190
        balao_rect.topleft = (pos_x, pos_y)
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - balao_inicio_tempo < balao_duracao:
            tela.blit(caixa, balao_rect)
            alocar_texto(tela, balao_texto, balao_rect)
        else:
            mostrar_balao = False
