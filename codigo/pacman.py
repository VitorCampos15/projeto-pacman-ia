import pygame
import sys
import os
import random
from fantasmas.blinky import Blinky
from fantasmas.pinky import Pinky
from fantasmas.inky import Inky
from fantasmas.clyde import Clyde


# Constantes
TAMANHO_BLOCO = 32
LARGURA = 28 * TAMANHO_BLOCO
ALTURA = 31 * TAMANHO_BLOCO
FPS = 60
BOLINHAS_PARA_AVANCAR = 35

# Cores
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)
BRANCO = (255, 255, 255)
VERDE = (0, 255, 0)
ROXO = (128, 0, 128)
AZUL_CLARO = (100, 100, 255)

# Carregamento do mapa
def carregar_mapa(caminho):
    mapa = []
    posicao_blinky = None
    posicao_pinky = None
    posicao_inky = None
    posicao_clyde = None
    posicoes_frutas = []

    with open(caminho, "r") as arquivo:
        for y, linha in enumerate(arquivo):
            linha = linha.strip()
            if not linha:
                continue

            linha_convertida = []
            for x, c in enumerate(linha):
                if c == '0':
                    linha_convertida.append(2) 
                elif c == '1':
                    linha_convertida.append(1) 
                elif c == '3':
                    posicao_blinky = (x * TAMANHO_BLOCO, y * TAMANHO_BLOCO)
                    linha_convertida.append(0)  
                elif c == '4':
                    posicao_pinky = (x * TAMANHO_BLOCO, y * TAMANHO_BLOCO)
                    linha_convertida.append(0)  
                elif c == '5':
                    posicao_inky = (x * TAMANHO_BLOCO, y * TAMANHO_BLOCO)
                    linha_convertida.append(0) 
                elif c == '6':
                    posicao_clyde = (x * TAMANHO_BLOCO, y * TAMANHO_BLOCO)
                    linha_convertida.append(0)                    
                else:
                    linha_convertida.append(0)
            mapa.append(linha_convertida)
    
    # Adicionando frutas (power-ups) em posições aleatórias
    frutas_adicionadas = 0
    while frutas_adicionadas < 4:  
        x = random.randint(1, len(mapa[0]) - 2)
        y = random.randint(1, len(mapa) - 2)
        if mapa[y][x] != 1:
            if mapa[y][x] == 2:  
                mapa[y][x] = 3  
                posicoes_frutas.append((x, y))
                frutas_adicionadas += 1

    return mapa, posicao_blinky, posicao_pinky, posicao_inky, posicao_clyde, posicoes_frutas


# Verifica se o movimento é possível
def pode_mover(x, y, mapa):
    pontos = [
        (x, y),
        (x + TAMANHO_BLOCO - 1, y),
        (x, y + TAMANHO_BLOCO - 1),
        (x + TAMANHO_BLOCO - 1, y + TAMANHO_BLOCO - 1)
    ]
    for px, py in pontos:
        grid_x = px // TAMANHO_BLOCO
        grid_y = py // TAMANHO_BLOCO
        if not (0 <= grid_y < len(mapa) and 0 <= grid_x < len(mapa[0])):
            return False
        if mapa[grid_y][grid_x] == 1:
            return False
    return True

def colisao(pac_x, pac_y, fant_x, fant_y):
    return abs(pac_x - fant_x) < 16 and abs(pac_y - fant_y) < 16

def verificar_bolinha_comida(mapa, mapa_original):
    for y, linha in enumerate(mapa):
        for x, bloco in enumerate(linha):
            if mapa_original[y][x] == 2 and bloco != 2:
                return True
    return False

def mostrar_game_over(tela):
    fonte = pygame.font.SysFont("arial", 48, bold=True)
    texto = fonte.render("GAME OVER", True, (255, 0, 0))
    texto_rect = texto.get_rect(center=(LARGURA // 2, ALTURA // 2))

    botao_fonte = pygame.font.SysFont("arial", 32, bold=True)
    botao_texto = botao_fonte.render("Tentar Novamente", True, (255, 255, 255))
    botao_rect = botao_texto.get_rect(center=(LARGURA // 2, ALTURA // 2 + 60))

    while True:
        tela.fill((0, 0, 0))
        tela.blit(texto, texto_rect)
        pygame.draw.rect(tela, (0, 0, 255), botao_rect.inflate(20, 10))
        tela.blit(botao_texto, botao_rect)
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_rect.collidepoint(evento.pos):
                    return  

def mostrar_conclusao(tela):
    fonte = pygame.font.SysFont("arial", 48, bold=True)
    texto = fonte.render("PARABÉNS!", True, VERDE)
    texto_rect = texto.get_rect(center=(LARGURA // 2, ALTURA // 2 - 60))
    
    subfonteTexto = pygame.font.SysFont("arial", 32, bold=False)
    subtexto = subfonteTexto.render("Você concluiu todos os níveis!", True, BRANCO)
    subtexto_rect = subtexto.get_rect(center=(LARGURA // 2, ALTURA // 2))

    botao_fonte = pygame.font.SysFont("arial", 32, bold=True)
    botao_texto = botao_fonte.render("Jogar Novamente", True, (255, 255, 255))
    botao_rect = botao_texto.get_rect(center=(LARGURA // 2, ALTURA // 2 + 80))

    while True:
        tela.fill(PRETO)
        tela.blit(texto, texto_rect)
        tela.blit(subtexto, subtexto_rect)
        pygame.draw.rect(tela, AZUL, botao_rect.inflate(20, 10))
        tela.blit(botao_texto, botao_rect)
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_rect.collidepoint(evento.pos):
                    return  

def carregar_proximo_nivel(nivel_atual):
    if nivel_atual == 1:
        return os.path.join(os.path.dirname(__file__), "nivel2", "mapa.txt"), 2
    elif nivel_atual == 2:
        return os.path.join(os.path.dirname(__file__), "nivel3", "mapa.txt"), 3
    else:
        return os.path.join(os.path.dirname(__file__), "nivel1", "mapa.txt"), 1
        
# Renderiza uma fruta na posição específica
def desenhar_fruta(tela, x, y):
    pygame.draw.circle(tela, (255, 0, 0), (x * TAMANHO_BLOCO + 16, y * TAMANHO_BLOCO + 18), 8)
    pygame.draw.line(tela, (0, 100, 0), 
                    (x * TAMANHO_BLOCO + 16, y * TAMANHO_BLOCO + 10), 
                    (x * TAMANHO_BLOCO + 16, y * TAMANHO_BLOCO + 4), 3)

def atualizar_fantasmas(mapa, pacman_pos, direcao, modo_fuga, tempo_modo_fuga):
    grid_x, grid_y = pacman_pos
    
    if modo_fuga:
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - tempo_modo_fuga > 8000:  
            modo_fuga = False
    
    if not modo_fuga:
        blinky.atualizar(mapa, pacman_pos)
    else:
        destino_fuga = (1, 1) 
        blinky.atualizar(mapa, destino_fuga)
    
    if not modo_fuga:
        pinky.atualizar(mapa, pacman_pos, direcao)
    else:
        pinky.atualizar(mapa, (1, 1), (0, 0))  
    
    if not modo_fuga:
        inky.atualizar(mapa, pacman_pos)
    else:
        inky.atualizar(mapa, (len(mapa[0])-2, 1)) 
    
    if not modo_fuga:
        clyde.atualizar(mapa, pacman_pos)
    else:
        clyde.atualizar(mapa, (len(mapa[0])-2, len(mapa)-2)) 
    
    return modo_fuga

# Inicialização
pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Pac-Man")
clock = pygame.time.Clock()

nivel_atual = 1
CAMINHO_MAPA = os.path.join(os.path.dirname(__file__), "nivel1", "mapa.txt")
MAPA, blinky_pos, pinky_pos, inky_pos, clyde_pos, posicoes_frutas = carregar_mapa(CAMINHO_MAPA)
MAPA_ORIGINAL = [linha[:] for linha in MAPA]  # Copia o mapa para comparação

pac_x = 1 * TAMANHO_BLOCO
pac_y = 1 * TAMANHO_BLOCO
velocidade = 2

blinky = Blinky(blinky_pos)
pinky = Pinky(pinky_pos)
inky = Inky(inky_pos)
clyde = Clyde(clyde_pos)

bolinhas_comidas = 0
modo_fuga = False
tempo_modo_fuga = 0

while True:
    clock.tick(FPS)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    teclas = pygame.key.get_pressed()
    direcao = (0, 0)

    if teclas[pygame.K_UP]:
        direcao = (0, -1)
        if pode_mover(pac_x, pac_y - velocidade, MAPA):
            pac_y -= velocidade
    elif teclas[pygame.K_DOWN]:
        direcao = (0, 1)
        if pode_mover(pac_x, pac_y + velocidade, MAPA):
            pac_y += velocidade
    elif teclas[pygame.K_LEFT]:
        direcao = (-1, 0)
        if pode_mover(pac_x - velocidade, pac_y, MAPA):
            pac_x -= velocidade
    elif teclas[pygame.K_RIGHT]:
        direcao = (1, 0)
        if pode_mover(pac_x + velocidade, pac_y, MAPA):
            pac_x += velocidade
            
    # Comer comida ou power-up
    grid_x = pac_x // TAMANHO_BLOCO
    grid_y = pac_y // TAMANHO_BLOCO
    
    if MAPA[grid_y][grid_x] == 2:  # Comida normal
        MAPA[grid_y][grid_x] = 0
        bolinhas_comidas += 1
    
    elif MAPA[grid_y][grid_x] == 3:  # Fruta (power-up)
        MAPA[grid_y][grid_x] = 0
        modo_fuga = True
        tempo_modo_fuga = pygame.time.get_ticks()

    # Verificação para avançar de nível
    if bolinhas_comidas >= BOLINHAS_PARA_AVANCAR:
        bolinhas_comidas = 0
        if nivel_atual == 3:  
            mostrar_conclusao(tela)
            nivel_atual = 1
            CAMINHO_MAPA = os.path.join(os.path.dirname(__file__), "nivel1", "mapa.txt")
        else:
            CAMINHO_MAPA, nivel_atual = carregar_proximo_nivel(nivel_atual)
        
        MAPA, blinky_pos, pinky_pos, inky_pos, clyde_pos, posicoes_frutas = carregar_mapa(CAMINHO_MAPA)
        MAPA_ORIGINAL = [linha[:] for linha in MAPA] 
        pac_x, pac_y = 1 * TAMANHO_BLOCO, 1 * TAMANHO_BLOCO
        blinky = Blinky(blinky_pos)
        pinky = Pinky(pinky_pos)
        inky = Inky(inky_pos)
        clyde = Clyde(clyde_pos)
        modo_fuga = False

    modo_fuga = atualizar_fantasmas(MAPA, (grid_x, grid_y), direcao, modo_fuga, tempo_modo_fuga)
    
    tela.fill(PRETO)
    for y, linha in enumerate(MAPA):
        for x, bloco in enumerate(linha):
            if bloco == 1:
                pygame.draw.rect(tela, AZUL, (x * TAMANHO_BLOCO, y * TAMANHO_BLOCO, TAMANHO_BLOCO, TAMANHO_BLOCO))
            elif bloco == 2:
                pygame.draw.circle(tela, BRANCO, (x * TAMANHO_BLOCO + 16, y * TAMANHO_BLOCO + 16), 4)
            elif bloco == 3:  # Desenhar frutas (power-ups)
                desenhar_fruta(tela, x, y)

    # Desenhar Pac-Man
    pygame.draw.circle(tela, AMARELO, (pac_x + 16, pac_y + 16), 10)
    
    if not modo_fuga:
        blinky.desenhar(tela)
        pinky.desenhar(tela)
        inky.desenhar(tela)
        clyde.desenhar(tela)
    else:
        # Desenhar fantasmas azuis (modo de fuga)
        pygame.draw.circle(tela, AZUL_CLARO, 
                          (blinky.x + TAMANHO_BLOCO // 2, blinky.y + TAMANHO_BLOCO // 2), 
                          TAMANHO_BLOCO // 2 - 4)
        
        pygame.draw.circle(tela, AZUL_CLARO, 
                          (pinky.x + TAMANHO_BLOCO // 2, pinky.y + TAMANHO_BLOCO // 2), 
                          TAMANHO_BLOCO // 2 - 4)
        
        pygame.draw.circle(tela, AZUL_CLARO, 
                          (inky.x + TAMANHO_BLOCO // 2, inky.y + TAMANHO_BLOCO // 2), 
                          TAMANHO_BLOCO // 2 - 4)
        
        pygame.draw.circle(tela, AZUL_CLARO, 
                          (clyde.x + TAMANHO_BLOCO // 2, clyde.y + TAMANHO_BLOCO // 2), 
                          TAMANHO_BLOCO // 2 - 4)

    # Verifica colisão com fantasmas
    if not modo_fuga:
        if (colisao(pac_x, pac_y, blinky.x, blinky.y) or 
            colisao(pac_x, pac_y, pinky.x, pinky.y) or 
            colisao(pac_x, pac_y, inky.x, inky.y) or 
            colisao(pac_x, pac_y, clyde.x, clyde.y)):
            mostrar_game_over(tela)
            nivel_atual = 1
            CAMINHO_MAPA = os.path.join(os.path.dirname(__file__), "nivel1", "mapa.txt")
            MAPA, blinky_pos, pinky_pos, inky_pos, clyde_pos, posicoes_frutas = carregar_mapa(CAMINHO_MAPA)
            MAPA_ORIGINAL = [linha[:] for linha in MAPA]
            pac_x, pac_y = 1 * TAMANHO_BLOCO, 1 * TAMANHO_BLOCO
            blinky = Blinky(blinky_pos)
            pinky = Pinky(pinky_pos)
            inky = Inky(inky_pos)
            clyde = Clyde(clyde_pos)
            bolinhas_comidas = 0
            modo_fuga = False

    fonte_info = pygame.font.SysFont("arial", 20, bold=True)
    texto_nivel = fonte_info.render(f"Nível: {nivel_atual}", True, BRANCO)
    texto_bolinhas = fonte_info.render(f"Bolinhas: {bolinhas_comidas}/{BOLINHAS_PARA_AVANCAR}", True, BRANCO)
    
    tela.blit(texto_nivel, (10, 10))
    tela.blit(texto_bolinhas, (10, 40))
    
    if modo_fuga:
        tempo_atual = pygame.time.get_ticks()
        tempo_restante = max(0, 8 - (tempo_atual - tempo_modo_fuga) // 1000)
        texto_poder = fonte_info.render(f"Power-Up: {tempo_restante}s", True, AZUL_CLARO)
        tela.blit(texto_poder, (10, 70))

    pygame.display.flip()