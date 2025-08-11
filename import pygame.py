import pygame
import sys

class Configuracoes:
    """Classe para armazenar todas as configurações do jogo"""
    
    def __init__(self):
        pygame.init()
        
        # Detecta resolução da tela do usuário
        info = pygame.display.Info()
        self.largura = info.current_w
        self.altura = info.current_h
        
        # Tamanho da tela
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Game UFPE_Alagada")
        
        # Configurações do chão
        self.altura_chao = self.altura // 4
        
        # Fontes e cores
        self.fonte_grande = pygame.font.SysFont("Arial", 70)
        self.fonte_media = pygame.font.SysFont("Arial", 50)
        self.fonte_jogo = pygame.font.SysFont(None, 80)
        self.branco = (255, 255, 255)
        self.cinza = (150, 150, 150)
        self.azul_claro = (100, 200, 255)
        
        # FPS
        self.fps = 60


class CarregadorRecursos:
    """Classe para carregar e gerenciar todos os recursos do jogo"""
    
    def __init__(self, config):
        self.config = config
        self.carregar_imagens()
    
    def carregar_imagens(self):
        """Carrega todas as imagens do jogo"""
        # Tela de início
        self.imagem_tela_inicio = pygame.image.load("images/tela_inicial.png")
        self.imagem_tela_inicio = pygame.transform.scale(self.imagem_tela_inicio, (self.config.largura, self.config.altura))
        
        # Botões
        self.jogar_buttom = pygame.image.load("images/jogar_buttom.png")
        self.jogar_buttom = pygame.transform.scale(self.jogar_buttom, (self.config.largura // 7, self.config.altura // 7))
        
        self.creditos_buttom = pygame.image.load("images/creditos_buttom.png")
        self.creditos_buttom = pygame.transform.scale(self.creditos_buttom, (self.config.largura // 7, self.config.altura // 7))
        
        self.sair_buttom = pygame.image.load("images/sair_buttom.png")
        self.sair_buttom = pygame.transform.scale(self.sair_buttom, (self.config.largura // 7, self.config.altura // 7))
        
        # Chão
        self.chao_sprite = pygame.image.load("images/chao_sprite.png")
        largura_chao = int(self.chao_sprite.get_width() * (self.config.altura_chao / self.chao_sprite.get_height()))
        self.chao_sprite = pygame.transform.scale(self.chao_sprite, (largura_chao, self.config.altura_chao))
        self.largura_chao = largura_chao
        
        # Cenários
        self.carregar_cenarios()
        
        # Personagem e itens
        self.carregar_personagem_e_itens()
    
    def carregar_cenarios(self):
        """Carrega os cenários do jogo"""
        caminhos_fundos = ["images/entrada_ufpe_2.png", "images/bib_central.png", "images/ru.png"]
        self.cenarios = []
        for caminho in caminhos_fundos:
            imagem = pygame.image.load(caminho)
            imagem = pygame.transform.scale(imagem, (self.config.largura, self.config.altura - self.config.altura_chao))
            self.cenarios.append(imagem)
    
    def carregar_personagem_e_itens(self):
        """Carrega o personagem e os itens coletáveis"""
        self.personagem_img = pygame.image.load("images/kakashi.png")
        self.personagem_img = pygame.transform.scale(self.personagem_img, (self.config.largura / 10, self.config.altura/10))
        
        self.bota_img = pygame.image.load("images/bota.png")
        self.bota_img = pygame.transform.scale(self.bota_img, (self.config.largura/15, self.config.altura/15))
        
        self.guarda_chuva_img = pygame.image.load("images/guarda_chuva.png")
        self.guarda_chuva_img = pygame.transform.scale(self.guarda_chuva_img, (self.config.largura/15, self.config.altura/15))


class Jogador:
    """Classe para gerenciar o jogador"""
    
    def __init__(self, config, recursos):
        self.config = config
        self.recursos = recursos
        self.resetar_posicao()
        self.velocidade = 10
    
    def resetar_posicao(self):
        """Reseta a posição do jogador para a posição inicial"""
        self.x = self.config.largura - 200
        self.y = self.config.altura - self.config.altura_chao - self.recursos.personagem_img.get_height()
        self.tamanho = 50
    
    def processar_movimento(self, teclas):
        """Processa o movimento do jogador baseado nas teclas pressionadas"""
        if teclas[pygame.K_LEFT]:
            self.x -= self.velocidade
        if teclas[pygame.K_RIGHT]:
            self.x += self.velocidade
        if teclas[pygame.K_UP]:
            self.y -= self.velocidade
        if teclas[pygame.K_DOWN]:
            self.y += self.velocidade
    
    def aplicar_limites_movimento(self):
        """Aplica os limites de movimento do jogador"""
        jogador_rect = pygame.Rect(self.x, self.y, self.recursos.personagem_img.get_width(), self.recursos.personagem_img.get_height())
        
        # Define os limites de movimento
        limite_x_min = 0
        limite_x_max = self.config.largura - self.recursos.personagem_img.get_width()
        limite_y_min = self.config.altura - self.config.altura_chao - self.recursos.personagem_img.get_height()
        limite_y_max = self.config.altura
        
        # Cria um retângulo de limites e usa clamp_ip
        limites_rect = pygame.Rect(limite_x_min, limite_y_min, limite_x_max - limite_x_min, limite_y_max - limite_y_min)
        jogador_rect.clamp_ip(limites_rect)
        
        # Atualiza as posições do jogador
        self.x = jogador_rect.x
        self.y = jogador_rect.y
        
        return limites_rect
    
    def obter_rect_colisao(self):
        """Retorna o retângulo de colisão do jogador"""
        return pygame.Rect(self.x, self.y, self.recursos.personagem_img.get_width(), self.recursos.personagem_img.get_height())
    
    def desenhar(self, tela):
        """Desenha o jogador na tela"""
        tela.blit(self.recursos.personagem_img, (self.x, self.y))


class GerenciadorItens:
    """Classe para gerenciar os itens coletáveis"""
    
    def __init__(self, config, recursos):
        self.config = config
        self.recursos = recursos
        self.resetar_itens()
    
    def resetar_itens(self):
        """Reseta o estado dos itens"""
        self.bota_visivel = True
        self.guarda_chuva_visivel = True
        self.cont_botas = 0
        self.cont_guarda_chuvas = 0
    
    def obter_posicao_bota(self):
        """Retorna a posição da bota"""
        return (150, self.config.altura - self.config.altura_chao + (self.recursos.bota_img.get_height() * 0.2))
    
    def obter_posicao_guarda_chuva(self):
        """Retorna a posição do guarda-chuva"""
        return (450, self.config.altura - self.config.altura_chao + (self.recursos.guarda_chuva_img.get_height() * 0.2))
    
    def obter_rect_bota(self):
        """Retorna o retângulo de colisão da bota"""
        pos_x, pos_y = self.obter_posicao_bota()
        return pygame.Rect(pos_x, pos_y, self.recursos.bota_img.get_width(), self.recursos.bota_img.get_height())
    
    def obter_rect_guarda_chuva(self):
        """Retorna o retângulo de colisão do guarda-chuva"""
        pos_x, pos_y = self.obter_posicao_guarda_chuva()
        return pygame.Rect(pos_x, pos_y, self.recursos.guarda_chuva_img.get_width(), self.recursos.guarda_chuva_img.get_height())
    
    def verificar_colisoes(self, jogador_rect):
        """Verifica colisões entre o jogador e os itens"""
        if jogador_rect.colliderect(self.obter_rect_bota()) and self.bota_visivel:
            self.cont_botas += 1
            self.bota_visivel = False
        
        if jogador_rect.colliderect(self.obter_rect_guarda_chuva()) and self.guarda_chuva_visivel:
            self.cont_guarda_chuvas += 1
            self.guarda_chuva_visivel = False
    
    def resetar_visibilidade(self):
        """Reseta a visibilidade dos itens (chamado ao trocar de cenário)"""
        self.bota_visivel = True
        self.guarda_chuva_visivel = True
    
    def desenhar(self, tela):
        """Desenha os itens na tela"""
        if self.bota_visivel:
            tela.blit(self.recursos.bota_img, self.obter_posicao_bota())
        if self.guarda_chuva_visivel:
            tela.blit(self.recursos.guarda_chuva_img, self.obter_posicao_guarda_chuva())
    
    def desenhar_rects_colisao(self, tela):
        """Desenha os retângulos de colisão dos itens"""
        if self.bota_visivel:
            pygame.draw.rect(tela, (0, 255, 0), self.obter_rect_bota(), 2)
        if self.guarda_chuva_visivel:
            pygame.draw.rect(tela, (0, 0, 255), self.obter_rect_guarda_chuva(), 2)


class GerenciadorCenarios:
    """Classe para gerenciar os cenários"""
    
    def __init__(self, recursos):
        self.recursos = recursos
        self.indice_atual = 0
        self.ultimo_cenario = 0
    
    def trocar_cenario_esquerda(self, jogador):
        """Troca para o próximo cenário quando o jogador vai para a esquerda"""
        if jogador.x < 0 and self.indice_atual < len(self.recursos.cenarios) - 1:
            self.indice_atual += 1
            jogador.x = self.recursos.config.largura - jogador.tamanho
            return True
        return False
    
    def trocar_cenario_direita(self, jogador):
        """Troca para o cenário anterior quando o jogador vai para a direita"""
        if jogador.x > self.recursos.config.largura - jogador.tamanho and self.indice_atual > 0:
            self.indice_atual -= 1
            jogador.x = 0
            return True
        return False
    
    def aplicar_limites_tela(self, jogador):
        """Aplica limites para o jogador não sair da tela"""
        if jogador.x < 0:
            jogador.x = 0
        if jogador.x > self.recursos.config.largura - jogador.tamanho:
            jogador.x = self.recursos.config.largura - jogador.tamanho
        
        if self.indice_atual == 0 and jogador.x > self.recursos.config.largura:
            jogador.x = self.recursos.config.largura
    
    def verificar_mudanca_cenario(self, gerenciador_itens):
        """Verifica se houve mudança de cenário e reseta os itens se necessário"""
        if self.ultimo_cenario != self.indice_atual:
            gerenciador_itens.resetar_visibilidade()
        self.ultimo_cenario = self.indice_atual
    
    def desenhar(self, tela):
        """Desenha o cenário atual"""
        tela.blit(self.recursos.cenarios[self.indice_atual], (0, 0))


class Interface:
    """Classe para gerenciar a interface do usuário"""
    
    def __init__(self, config):
        self.config = config
    
    def desenhar_chao(self, tela, recursos):
        """Desenha o chão repetindo a textura horizontalmente"""
        posicao_y = self.config.altura - self.config.altura_chao
        
        num_repeticoes = self.config.largura // recursos.largura_chao + 1
        
        for i in range(num_repeticoes):
            posicao_x = i * recursos.largura_chao
            tela.blit(recursos.chao_sprite, (posicao_x, posicao_y))
    
    def desenhar_botao(self, tela, img_buttom, x, y, acao=None):
        """Desenha um botão com efeito hover"""
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        largura_buttom = img_buttom.get_width()
        altura_buttom = img_buttom.get_height()
        
        if x < mouse[0] < x + largura_buttom and y < mouse[1] < y + altura_buttom:
            botao_ampliado = pygame.transform.scale(img_buttom, (int(largura_buttom * 1.05), int(altura_buttom * 1.05)))
            tela.blit(botao_ampliado, (x - 5, y - 5))
            
            if click[0] == 1 and acao is not None:
                pygame.time.delay(200)
                acao()
        else:
            tela.blit(img_buttom, (x, y))
    
    def desenhar_hud(self, tela, gerenciador_itens):
        """Desenha o HUD com informações do jogador"""
        texto = self.config.fonte_jogo.render(f"Botas: {gerenciador_itens.cont_botas}  Guarda chuvas: {gerenciador_itens.cont_guarda_chuvas}", True, self.config.branco)
        tela.blit(texto, (100, 100))
    
    def desenhar_rects_debug(self, tela, jogador_rect, limites_rect):
        """Desenha retângulos de debug"""
        pygame.draw.rect(tela, (255, 0, 0), jogador_rect, 2)  # Vermelho para o jogador
        pygame.draw.rect(tela, (255, 255, 255), limites_rect, 1)  # Branco para os limites


class Jogo:
    """Classe principal do jogo"""
    
    def __init__(self):
        self.config = Configuracoes()
        self.recursos = CarregadorRecursos(self.config)
        self.interface = Interface(self.config)
        self.jogador = Jogador(self.config, self.recursos)
        self.gerenciador_itens = GerenciadorItens(self.config, self.recursos)
        self.gerenciador_cenarios = GerenciadorCenarios(self.recursos)
        self.clock = pygame.time.Clock()
    
    def processar_eventos(self):
        """Processa eventos do pygame"""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
    def atualizar_jogo(self):
        """Atualiza o estado do jogo"""
        teclas = pygame.key.get_pressed()
        
        # Processa movimento do jogador
        self.jogador.processar_movimento(teclas)
        
        # Troca de cenários
        self.gerenciador_cenarios.trocar_cenario_esquerda(self.jogador)
        self.gerenciador_cenarios.trocar_cenario_direita(self.jogador)
        
        # Aplica limites
        self.gerenciador_cenarios.aplicar_limites_tela(self.jogador)
        limites_rect = self.jogador.aplicar_limites_movimento()
        
        # Verifica colisões
        jogador_rect = self.jogador.obter_rect_colisao()
        self.gerenciador_itens.verificar_colisoes(jogador_rect)
        
        # Verifica mudança de cenário
        self.gerenciador_cenarios.verificar_mudanca_cenario(self.gerenciador_itens)
        
        return jogador_rect, limites_rect
    
    def desenhar(self, jogador_rect, limites_rect):
        """Desenha todos os elementos do jogo"""
        # Desenha cenário e chão
        self.gerenciador_cenarios.desenhar(self.config.tela)
        self.interface.desenhar_chao(self.config.tela, self.recursos)
        
        # Desenha jogador e itens
        self.jogador.desenhar(self.config.tela)
        self.gerenciador_itens.desenhar(self.config.tela)
        
        # Desenha interface
        self.interface.desenhar_hud(self.config.tela, self.gerenciador_itens)
        self.interface.desenhar_rects_debug(self.config.tela, jogador_rect, limites_rect)
        self.gerenciador_itens.desenhar_rects_colisao(self.config.tela)
    
    def executar(self):
        """Executa o loop principal do jogo"""
        while True:
            self.processar_eventos()
            jogador_rect, limites_rect = self.atualizar_jogo()
            self.desenhar(jogador_rect, limites_rect)
            
            pygame.display.flip()
            self.clock.tick(self.config.fps)

