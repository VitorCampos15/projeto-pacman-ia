import pygame
import heapq

# Pinky (rosa) - "Speedy"
# Comportamento:
# Usa busca gulosa para tentar antecipar o movimento do Pac-Man.
# O destino alvo é uma posição alguns blocos à frente da direção atual do jogador.
# Tenta cortar caminho e encurralar o jogador.


ROSA = (255, 105, 180)
TAMANHO_BLOCO = 32

class Pinky:
    def __init__(self, pos_inicial):
        self.x, self.y = pos_inicial
        self.grid_x = self.x // TAMANHO_BLOCO
        self.grid_y = self.y // TAMANHO_BLOCO
        self.caminho = []
        self.velocidade = 2
        self.destino_pixel = None

    def desenhar(self, tela):
        pygame.draw.circle(
            tela,
            ROSA,
            (self.x + TAMANHO_BLOCO // 2, self.y + TAMANHO_BLOCO // 2),
            TAMANHO_BLOCO // 2 - 4
        )

    def atualizar(self, mapa, pac_pos, direcao):
        destino_previsto = (
            pac_pos[0] + direcao[0] * 4,
            pac_pos[1] + direcao[1] * 4
        )
        destino_previsto = self.clamp_destino(destino_previsto, mapa)

        if self.destino_pixel is None or (self.x, self.y) == self.destino_pixel:
            if not self.caminho:
                self.grid_x = self.x // TAMANHO_BLOCO
                self.grid_y = self.y // TAMANHO_BLOCO
                self.caminho = self.busca_gulosa(mapa, (self.grid_x, self.grid_y), destino_previsto)

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

    def busca_gulosa(self, mapa, inicio, fim):
        abertos = [(self.heuristica(inicio, fim), inicio)]
        came_from = {}

        visitados = set()

        while abertos:
            _, atual = heapq.heappop(abertos)
            if atual == fim:
                caminho = []
                while atual != inicio:
                    caminho.insert(0, atual)
                    atual = came_from[atual]
                return caminho

            visitados.add(atual)
            for vizinho in self.vizinhos_validos(atual, mapa):
                if vizinho in visitados:
                    continue
                if vizinho not in came_from:
                    came_from[vizinho] = atual
                    heapq.heappush(abertos, (self.heuristica(vizinho, fim), vizinho))

        return []

    def heuristica(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan

    def vizinhos_validos(self, pos, mapa):
        x, y = pos
        vizinhos = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= ny < len(mapa) and 0 <= nx < len(mapa[0]) and mapa[ny][nx] != 1:
                vizinhos.append((nx, ny))
        return vizinhos

    def clamp_destino(self, destino, mapa):
        x, y = destino
        x = max(0, min(len(mapa[0]) - 1, x))
        y = max(0, min(len(mapa) - 1, y))
        return (x, y)
