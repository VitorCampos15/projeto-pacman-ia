# Inky (azul) - "Bashful"
# Comportamento:
# Move-se de forma imprevisível, combinando a posição do Pac-Man com a do Blinky.
# Seu alvo é calculado com base em uma fórmula: posição do Pac-Man + vetor até Blinky.
# O resultado é um comportamento errático e difícil de prever.
import pygame
import heapq

AZUL = (0, 255, 255)
TAMANHO_BLOCO = 32

class Inky:
    def __init__(self, pos_inicial):
        self.x, self.y = pos_inicial
        self.grid_x = self.x // TAMANHO_BLOCO
        self.grid_y = self.y // TAMANHO_BLOCO
        self.caminho = []
        self.velocidade = 2
        self.destino_pixel = None
        self.modo = 'perseguir'  # alterna entre 'perseguir' e 'fugir'
        self.tempo_modo = pygame.time.get_ticks()

    def desenhar(self, tela):
        pygame.draw.circle(
            tela,
            AZUL,
            (self.x + TAMANHO_BLOCO // 2, self.y + TAMANHO_BLOCO // 2),
            TAMANHO_BLOCO // 2 - 4
        )

    def atualizar(self, mapa, pac_pos):
        agora = pygame.time.get_ticks()
        if agora - self.tempo_modo > 5000:  # alterna a cada 5 segundos
            self.modo = 'fugir' if self.modo == 'perseguir' else 'perseguir'
            self.tempo_modo = agora

        # destino depende do modo
        if self.modo == 'perseguir':
            destino = pac_pos
        else:
            destino = (1, len(mapa)-2)  # canto inferior esquerdo

        if self.destino_pixel is None or (self.x, self.y) == self.destino_pixel:
            if not self.caminho:
                self.grid_x = self.x // TAMANHO_BLOCO
                self.grid_y = self.y // TAMANHO_BLOCO
                self.caminho = self.a_estrela(mapa, (self.grid_x, self.grid_y), destino)

            if self.caminho:
                prox = self.caminho.pop(0)
                self.destino_pixel = (prox[0] * TAMANHO_BLOCO, prox[1] * TAMANHO_BLOCO)

        if self.destino_pixel:
            dx = self.destino_pixel[0] - self.x
            dy = self.destino_pixel[1] - self.y

            if dx != 0:
                self.x += self.velocidade * (1 if dx > 0 else -1)
            elif dy != 0:
                self.y += self.velocidade * (1 if dy > 0 else -1)

            if abs(dx) < self.velocidade:
                self.x = self.destino_pixel[0]
            if abs(dy) < self.velocidade:
                self.y = self.destino_pixel[1]

    def a_estrela(self, mapa, inicio, fim):
        abertos = [(0, inicio)]
        came_from = {}
        g = {inicio: 0}

        while abertos:
            _, atual = heapq.heappop(abertos)

            if atual == fim:
                caminho = []
                while atual != inicio:
                    caminho.insert(0, atual)
                    atual = came_from[atual]
                return caminho

            for vizinho in self.vizinhos_validos(atual, mapa):
                custo = g[atual] + 1
                if vizinho not in g or custo < g[vizinho]:
                    g[vizinho] = custo
                    prioridade = custo + self.heuristica(vizinho, fim)
                    heapq.heappush(abertos, (prioridade, vizinho))
                    came_from[vizinho] = atual

        return []

    def heuristica(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def vizinhos_validos(self, pos, mapa):
        x, y = pos
        vizinhos = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= ny < len(mapa) and 0 <= nx < len(mapa[0]) and mapa[ny][nx] != 1:
                vizinhos.append((nx, ny))
        return vizinhos
