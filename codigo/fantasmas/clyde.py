# Clyde (laranja) - "Pokey"
# Comportamento:
# Persegue o Pac-Man como o Blinky, mas se aproximar demais (menos de 8 blocos), foge para uma região fixa do mapa.
# Alterna entre perseguição e fuga, criando padrões únicos.
import pygame
import heapq

LARANJA = (255, 165, 0)
TAMANHO_BLOCO = 32

class Clyde:
    def __init__(self, pos_inicial):
        self.x, self.y = pos_inicial
        self.grid_x = self.x // TAMANHO_BLOCO
        self.grid_y = self.y // TAMANHO_BLOCO
        self.caminho = []
        self.velocidade = 1.8
        self.destino_pixel = None

    def desenhar(self, tela):
        pygame.draw.circle(
            tela,
            LARANJA,
            (self.x + TAMANHO_BLOCO // 2, self.y + TAMANHO_BLOCO // 2),
            TAMANHO_BLOCO // 2 - 4
        )

    def atualizar(self, mapa, pac_pos):
        # Decide destino com base na distância ao Pac-Man
        dist = self.heuristica((self.x // TAMANHO_BLOCO, self.y // TAMANHO_BLOCO), pac_pos)
        if dist > 8:
            destino = pac_pos
        else:
            destino = (len(mapa[0]) - 2, len(mapa) - 2)  # canto inferior direito

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
