# musica_config.py
# Arquivo para gerenciar a música do jogo de forma compartilhada

import pygame

# Variáveis globais para controle de música
musica_jogo = None
musica_jogo_playing = False
musica_combate = None
musica_combate_playing = False
som_ataque = None
som_ataque_inimigo = None
som_vitoria = None

def inicializar_musica_jogo():
    """Inicializa a música de fundo do jogo"""
    global musica_jogo
    try:
        musica_jogo = pygame.mixer.Sound("SFX/Who Was I_.mp3")
        musica_jogo.set_volume(0.25)
        print("Música do jogo inicializada")
        return True
    except Exception as e:
        print(f"Erro ao inicializar música do jogo: {e}")
        return False

def inicializar_musica_combate():
    """Inicializa a música de combate"""
    global musica_combate
    try:
        musica_combate = pygame.mixer.Sound("SFX/Unexpectancy, Pt. 1.mp3")
        musica_combate.set_volume(0.3)  # Volume um pouco mais alto para combate
        print("Música de combate inicializada")
        return True
    except Exception as e:
        print(f"Erro ao inicializar música de combate: {e}")
        return False

def inicializar_som_ataque():
    """Inicializa o som de ataque"""
    global som_ataque
    try:
        som_ataque = pygame.mixer.Sound("SFX/hitmarker_2.mp3")
        som_ataque.set_volume(0.4)  # Volume para o som de ataque
        print("Som de ataque inicializado")
        return True
    except Exception as e:
        print(f"Erro ao inicializar som de ataque: {e}")
        return False

def inicializar_som_ataque_inimigo():
    """Inicializa o som de ataque do inimigo"""
    global som_ataque_inimigo
    try:
        som_ataque_inimigo = pygame.mixer.Sound("SFX/hitmarker_2.mp3")  # Usando o mesmo som por enquanto
        som_ataque_inimigo.set_volume(0.35)  # Volume um pouco mais baixo que o ataque do jogador
        print("Som de ataque do inimigo inicializado")
        return True
    except Exception as e:
        print(f"Erro ao inicializar som de ataque do inimigo: {e}")
        return False

def inicializar_som_vitoria():
    """Inicializa o som de vitória"""
    global som_vitoria
    try:
        som_vitoria = pygame.mixer.Sound("SFX/hitmarker_2.mp3")  # Usando o mesmo som por enquanto
        som_vitoria.set_volume(0.5)  # Volume mais alto para celebrar a vitória
        print("Som de vitória inicializado")
        return True
    except Exception as e:
        print(f"Erro ao inicializar som de vitória: {e}")
        return False

def tocar_musica_jogo():
    """Toca a música de fundo do jogo em loop"""
    global musica_jogo, musica_jogo_playing
    if musica_jogo and not musica_jogo_playing:
        musica_jogo.play(-1)
        musica_jogo_playing = True
        print("Música do jogo iniciada em loop")

def parar_musica_jogo():
    """Para a música de fundo do jogo"""
    global musica_jogo, musica_jogo_playing
    if musica_jogo and musica_jogo_playing:
        musica_jogo.stop()
        musica_jogo_playing = False
        print("Música do jogo pausada")

def retomar_musica_jogo():
    """Retoma a música de fundo do jogo"""
    global musica_jogo, musica_jogo_playing
    if musica_jogo and not musica_jogo_playing:
        musica_jogo.play(-1)
        musica_jogo_playing = True
        print("Música do jogo retomada")

def tocar_musica_combate():
    """Toca a música de combate em loop"""
    global musica_combate, musica_combate_playing
    if musica_combate and not musica_combate_playing:
        musica_combate.play(-1)
        musica_combate_playing = True
        print("Música de combate iniciada")

def parar_musica_combate():
    """Para a música de combate"""
    global musica_combate, musica_combate_playing
    if musica_combate and musica_combate_playing:
        musica_combate.stop()
        musica_combate_playing = False
        print("Música de combate pausada")

def tocar_som_ataque():
    """Toca o som de ataque"""
    global som_ataque
    if som_ataque:
        som_ataque.play()
        print("Som de ataque tocado")

def tocar_som_ataque_inimigo():
    """Toca o som de ataque do inimigo"""
    global som_ataque_inimigo
    if som_ataque_inimigo:
        som_ataque_inimigo.play()
        print("Som de ataque do inimigo tocado")

def tocar_som_vitoria():
    """Toca o som de vitória"""
    global som_vitoria
    if som_vitoria:
        som_vitoria.play()
        print("Som de vitória tocado")
