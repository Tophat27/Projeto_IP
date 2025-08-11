# coleta.py
# Manages collectible items and their interactions with the player.

import pygame
from variaveis import *
from tela import *

tela_return = tela()
pygame.init()
largura, altura = get_size()

bota_img = pygame.image.load("images/bota.png")
bota_img = pygame.transform.scale(bota_img, (largura/15, altura/15))

guarda_chuva_img = pygame.image.load("images/guarda_chuva.png")
guarda_chuva_img = pygame.transform.scale(guarda_chuva_img, (largura/15, altura/15))

cracha_img = pygame.image.load("images/cracha_cininho.png")
cracha_img = pygame.transform.scale(cracha_img, (largura/15, altura/5))

def coletaveis(indice_cenario, ultimo_cenario, jogador_x, jogador_y, personagem_img, bota_visivel, guarda_chuva_visivel, inventory):
    bota_posc = 150
    guarda_chuva_posc = 450
    # Set chao to the top of the player's movement area (bottom 1/3 of screen)
    area_movimento = altura // 4
    chao = altura - area_movimento  # Align with the top of the movement area
    bota_rect = None
    guarda_chuva_rect = None

    if indice_cenario == 0:
        if bota_visivel:
            tela_return.blit(bota_img, (bota_posc, chao))
            bota_rect = pygame.Rect(bota_posc, chao, bota_img.get_width(), bota_img.get_height())
        if guarda_chuva_visivel:
            tela_return.blit(guarda_chuva_img, (guarda_chuva_posc, chao))
            guarda_chuva_rect = pygame.Rect(guarda_chuva_posc, chao, guarda_chuva_img.get_width(), guarda_chuva_img.get_height())

    if indice_cenario == 1:
        bota_posc = 800
        guarda_chuva_posc = 150
        if bota_visivel:
            tela_return.blit(bota_img, (bota_posc, chao))
            bota_rect = pygame.Rect(bota_posc, chao, bota_img.get_width(), bota_img.get_height())
        if guarda_chuva_visivel:
            tela_return.blit(guarda_chuva_img, (guarda_chuva_posc, chao))
            guarda_chuva_rect = pygame.Rect(guarda_chuva_posc, chao, guarda_chuva_img.get_width(), guarda_chuva_img.get_height())

    if indice_cenario == 2:
        bota_posc = 300
        guarda_chuva_posc = 200
        if bota_visivel:
            tela_return.blit(bota_img, (bota_posc, chao))
            bota_rect = pygame.Rect(bota_posc, chao, bota_img.get_width(), bota_img.get_height())
        if guarda_chuva_visivel:
            tela_return.blit(guarda_chuva_img, (guarda_chuva_posc, chao))
            guarda_chuva_rect = pygame.Rect(guarda_chuva_posc, chao, guarda_chuva_img.get_width(), guarda_chuva_img.get_height())

    if indice_cenario == 3:
        tela_return.blit(cracha_img, (600, chao))  # Also adjust cracha position

    ret_jogador = pygame.Rect(jogador_x, jogador_y, personagem_img.get_width(), personagem_img.get_height())
    if bota_rect and ret_jogador.colliderect(bota_rect) and bota_visivel:
        inventory.add_item("Boots")
        bota_visivel = False
    if guarda_chuva_rect and ret_jogador.colliderect(guarda_chuva_rect) and guarda_chuva_visivel:
        inventory.add_item("Umbrella")
        guarda_chuva_visivel = False

    if ultimo_cenario != indice_cenario:
        guarda_chuva_visivel = True
        bota_visivel = True

    return bota_rect, guarda_chuva_rect, bota_visivel, guarda_chuva_visivel