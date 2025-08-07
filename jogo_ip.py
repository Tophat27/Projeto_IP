import pygame
import sys

ultimo_x = 0
ultimo_cenario = 0
bota_visivel = True
guarda_chuva_visivel = True
cont_botas = 0
cont_guarda_chuvas = 0

pygame.init()

# Detecta resolução da tela do usuário
info = pygame.display.Info()
largura = info.current_w
altura = info.current_h

# Tamanho da tela
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Game UFPE_Alagada")

# Tela de início (imagem)
imagem_tela_inicio = pygame.image.load("images/tela_inicial.png")
imagem_tela_inicio = pygame.transform.scale(imagem_tela_inicio, (largura, altura))

# Carregando botões
jogar_buttom = pygame.image.load("images/jogar_buttom.png")
jogar_buttom = pygame.transform.scale(jogar_buttom, (largura // 7, altura // 7))

creditos_buttom = pygame.image.load("images/creditos_buttom.png")
creditos_buttom = pygame.transform.scale(creditos_buttom, (largura // 7, altura // 7))

sair_buttom = pygame.image.load("images/sair_buttom.png")
sair_buttom = pygame.transform.scale(sair_buttom, (largura // 7, altura // 7))

# Fontes e cores
fonte_grande = pygame.font.SysFont("Arial", 70)
fonte_media = pygame.font.SysFont("Arial", 50)
branco = (255, 255, 255)
cinza = (150, 150, 150)
azul_claro = (100, 200, 255)


def desenhar_botao(img_buttom, x, y, acao=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    largura_buttom = img_buttom.get_width()
    altura_buttom = img_buttom.get_height()

    #Verifica se mouse está sobre o botão
    if x < mouse[0] < x + largura_buttom and y < mouse[1] < y + altura_buttom:
        botao_ampliado = pygame.transform.scale(img_buttom, (int(largura_buttom * 1.05), int(altura_buttom * 1.05)))
        tela.blit(botao_ampliado, (x - 5, y - 5))  # desenha botão maior, centralizado
        
        if click[0] == 1 and acao is not None:
            pygame.time.delay(200)  # evita clique duplo
            acao()
    else:
        tela.blit(img_buttom, (x, y))



def mostrar_creditos():
    mostrando = True
    while mostrando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                mostrando = False

        tela.fill((0, 0, 0))
        texto = fonte_grande.render("Créditos", True, branco)
        texto_nome = fonte_media.render("Desenvolvido por Pedro (phhs)", True, branco)
        texto_esc = fonte_media.render("Pressione ESC para voltar", True, branco)

        tela.blit(texto, (largura // 2 - 150, 100))
        tela.blit(texto_nome, (largura // 2 - 300, 300))
        tela.blit(texto_esc, (largura // 2 - 250, 500))

        pygame.display.flip()
                

def iniciar_jogo():

    ultimo_x = 0
    ultimo_cenario = 0
    bota_visivel = True
    guarda_chuva_visivel = True
    cont_botas = 0
    cont_guarda_chuvas = 0

    # Cenarios
    caminhos_fundos = ["images/entrada_ufpe_2.png", "images/bib_central.png", "images/ru.png"]
    cenarios = []
    for caminho in caminhos_fundos:
        imagem = pygame.image.load(caminho)
        imagem = pygame.transform.scale(imagem, (largura, altura))
        cenarios.append(imagem)

    #Carregando personagem
    personagem_img = pygame.image.load("images/kakashi.png")
    personagem_img = pygame.transform.scale(personagem_img, (largura / 10, altura/10))

    bota_img = pygame.image.load("images/bota.png")
    bota_img = pygame.transform.scale(bota_img, (largura/15, altura/15))

    guarda_chuva_img = pygame.image.load("images/guarda_chuva.png")
    guarda_chuva_img = pygame.transform.scale(guarda_chuva_img, (largura/15, altura/15))

    indice_cenario = 0  # Começa no primeiro cenário

    # Jogador
    jogador_tamanho = 50
    jogador_x = largura - 200
    jogador_y = altura
    velocidade = 10

    clock = pygame.time.Clock()
    fps = 60

    fonte = pygame.font.SysFont(None, 80)

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
        if bota_visivel:
            tela.blit(bota_img, (150, 610))

        if guarda_chuva_visivel:
            tela.blit(guarda_chuva_img, (450, 610))

        texto = fonte.render(f"Botas: {cont_botas}  Guarda chuvas {cont_guarda_chuvas}", True, (255, 255, 255))  # Cor branca
        tela.blit(texto, (100, 100)) 


        ret_jogador = pygame.Rect(jogador_x, jogador_y, personagem_img.get_width(), personagem_img.get_height())
        ret_bota = pygame.Rect(150, 610, bota_img.get_width(), bota_img.get_height())
        ret_guarda_chuva = pygame.Rect(450, 610, guarda_chuva_img.get_width(), guarda_chuva_img.get_height())


        if ret_jogador.colliderect(ret_bota) and bota_visivel:
            cont_botas += 1
            bota_visivel = False
        if ret_jogador.colliderect(ret_guarda_chuva) and guarda_chuva_visivel:
            cont_guarda_chuvas += 1
            guarda_chuva_visivel = False

        if ultimo_cenario != indice_cenario:
            guarda_chuva_visivel = True
            bota_visivel = True
        ultimo_cenario = indice_cenario

        pygame.display.flip()
        clock.tick(fps)



# Tela de menu principal
def menu_principal():
    while True:
        tela.blit(imagem_tela_inicio, (0, 0))

        desenhar_botao(jogar_buttom, largura // 2 - 150, altura // 2 - 100, iniciar_jogo)
        desenhar_botao(creditos_buttom, largura // 2 - 150, altura // 2 + 0, mostrar_creditos)
        desenhar_botao(sair_buttom, largura // 2 - 150, altura // 2 + 100, pygame.quit)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()

# Inicia o menu
menu_principal()