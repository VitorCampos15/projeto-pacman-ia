import pygame
import sys
import os
from fantasmas.blinky import Blinky
from fantasmas.pinky import Pinky
from fantasmas.inky import Inky
from fantasmas.clyde import Clyde


# Constantes
TAMANHO_BLOCO = 32
LARGURA = 28 * TAMANHO_BLOCO
ALTURA = 31 * TAMANHO_BLOCO
FPS = 60

# Cores
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)
BRANCO = (255, 255, 255)

# Carregamento do mapa
def carregar_mapa(caminho):
    mapa = []
    posicao_blinky = None
    posicao_pinky = None

    with open(caminho, "r") as arquivo:
        for y, linha in enumerate(arquivo):
            linha = linha.strip()
            if not linha:
                continue

            linha_convertida = []
            for x, c in enumerate(linha):
                if c == '0':
                    linha_convertida.append(2)  # comida
                elif c == '1':
                    linha_convertida.append(1)  # parede
                elif c == '3':
                    posicao_blinky = (x * TAMANHO_BLOCO, y * TAMANHO_BLOCO)
                    linha_convertida.append(0)  # espaço livre
                elif c == '4':
                    posicao_pinky = (x * TAMANHO_BLOCO, y * TAMANHO_BLOCO)
                    linha_convertida.append(0)  # espaço livre
                elif c == '5':
                    posicao_inky = (x * TAMANHO_BLOCO, y * TAMANHO_BLOCO)
                    linha_convertida.append(0)  # espaço livre
                elif c == '6':
                    posicao_clyde = (x * TAMANHO_BLOCO, y * TAMANHO_BLOCO)
                    linha_convertida.append(0)  # espaço livre                    
                else:
                    linha_convertida.append(0)
            mapa.append(linha_convertida)

    return mapa, posicao_blinky, posicao_pinky, posicao_inky, posicao_clyde


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

# Início do jogo
CAMINHO_MAPA = os.path.join(os.path.dirname(__file__), "nivel1", "mapa.txt")

MAPA, blinky_pos, pinky_pos, inky_pos, clyde_pos = carregar_mapa(CAMINHO_MAPA)

blinky = Blinky(blinky_pos)
pinky = Pinky(pinky_pos)
inky = Inky(inky_pos)
clyde = Clyde(clyde_pos)

pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Pac-Man")
clock = pygame.time.Clock()

pac_x = 1 * TAMANHO_BLOCO
pac_y = 1 * TAMANHO_BLOCO
velocidade = 2
# --- Função de colisão (fora do loop) ---
def colisao(pac_x, pac_y, fant_x, fant_y):
    return abs(pac_x - fant_x) < 16 and abs(pac_y - fant_y) < 16

def mostrar_game_over(tela):
    fonte = pygame.font.SysFont("arial", 48, bold=True)
    texto = fonte.render("GAME OVER", True, (255, 0, 0))
    texto_rect = texto.get_rect(center=(LARGURA // 2, ALTURA // 2))

    tela.fill((0, 0, 0))
    tela.blit(texto, texto_rect)
    pygame.display.flip()

    # Espera 3 segundos antes de sair
    pygame.time.delay(3000)
    pygame.quit()
    sys.exit()



# Loop principal
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


    # Comer comida
    grid_x = pac_x // TAMANHO_BLOCO
    grid_y = pac_y // TAMANHO_BLOCO
    if MAPA[grid_y][grid_x] == 2:
        MAPA[grid_y][grid_x] = 0

    # Atualizar e desenhar tudo
    tela.fill(PRETO)
    for y, linha in enumerate(MAPA):
        for x, bloco in enumerate(linha):
            if bloco == 1:
                pygame.draw.rect(tela, AZUL, (x * TAMANHO_BLOCO, y * TAMANHO_BLOCO, TAMANHO_BLOCO, TAMANHO_BLOCO))
            elif bloco == 2:
                pygame.draw.circle(tela, BRANCO, (x * TAMANHO_BLOCO + 16, y * TAMANHO_BLOCO + 16), 4)

    pygame.draw.circle(tela, AMARELO, (pac_x + 16, pac_y + 16), 10)
    # Atualizar e desenhar Blinky
    pac_grid = (pac_x // TAMANHO_BLOCO, pac_y // TAMANHO_BLOCO)
    blinky.atualizar(MAPA, pac_grid)
    blinky.desenhar(tela)

    # Atualizar e desenhar Pinky
    pinky.atualizar(MAPA, (grid_x, grid_y), direcao)
    pinky.desenhar(tela)

    # Atualiza e desenha inky
    inky.atualizar(MAPA, (grid_x, grid_y))
    inky.desenhar(tela)

    # Atualiza e desenha clyde
    clyde.atualizar(MAPA, (grid_x, grid_y))
    clyde.desenhar(tela)


    if colisao(pac_x, pac_y, blinky.x, blinky.y):
        mostrar_game_over(tela)

    if colisao(pac_x, pac_y, pinky.x, pinky.y):
        mostrar_game_over(tela)

    if colisao(pac_x, pac_y, inky.x, inky.y):
        mostrar_game_over(tela)

    if colisao(pac_x, pac_y, clyde.x, clyde.y):
        mostrar_game_over(tela)



    pygame.display.flip()
