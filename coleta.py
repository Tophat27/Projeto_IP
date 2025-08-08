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
cracha_img = pygame.transform.scale(cracha_img,(largura/15, altura/5))

def coletaveis(indice_cenario, ultimo_cenario, jogador_x, jogador_y, personagem_img, bota_visivel, guarda_chuva_visivel, cont_botas, cont_guarda_chuvas):
    
    bota_posc = 150
    guarda_chuva_posc = 450
    chao = 610

    if indice_cenario == 0:
        if bota_visivel:
            tela_return.blit(bota_img, (bota_posc, chao))
        if guarda_chuva_visivel:
            tela_return.blit(guarda_chuva_img, (guarda_chuva_posc, chao))

    if indice_cenario == 1:
        bota_posc = 800
        guarda_chuva_posc = 150
        if bota_visivel:
            tela_return.blit(bota_img, (bota_posc, chao))
        if guarda_chuva_visivel:
            tela_return.blit(guarda_chuva_img, (guarda_chuva_posc, chao))

    if indice_cenario == 2:
        bota_posc = 300
        guarda_chuva_posc = 200
        if bota_visivel:
            tela_return.blit(bota_img, (bota_posc, chao))
        if guarda_chuva_visivel:
            tela_return.blit(guarda_chuva_img, (guarda_chuva_posc, chao))

    if indice_cenario == 3:
        tela_return.blit(cracha_img,(600,300))
    

    ret_jogador = pygame.Rect(jogador_x, jogador_y, personagem_img.get_width(), personagem_img.get_height())
    ret_bota = pygame.Rect(bota_posc, 610, bota_img.get_width(), bota_img.get_height())
    ret_guarda_chuva = pygame.Rect(guarda_chuva_posc, 610, guarda_chuva_img.get_width(), guarda_chuva_img.get_height())

    if ret_jogador.colliderect(ret_bota) and bota_visivel:
        cont_botas += 1
        bota_visivel = False
    if ret_jogador.colliderect(ret_guarda_chuva) and guarda_chuva_visivel:
        cont_guarda_chuvas += 1
        guarda_chuva_visivel = False

    if ultimo_cenario != indice_cenario:
        guarda_chuva_visivel = True
        bota_visivel = True
    
    return cont_botas, cont_guarda_chuvas,bota_visivel, guarda_chuva_visivel



