import pygame
import sys
import math
import random

# ======================
# FUNÇÃO PRINCIPAL (chamada pelo test.py)
# ======================
def minigame_equilibrio(calorias):
    pygame.init()

    LARGURA, ALTURA = 600, 400
    TELA = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Equilíbrio na Cobra")
    clock = pygame.time.Clock()

    # Número de segmentos baseado nas calorias (igual ao dinossauro)
    num_segmentos = 6

    class CobraEquilibrio:
        def __init__(self, num_seg):
            self.tamanho_celula = 20
            self.num_segmentos = num_seg
            self.pivo = (LARGURA // 2, ALTURA - 100)  # base da cobra

            # Posições relativas ao pivô (crescem para cima, y negativo)
            self.rel_pos = [(0, -i * self.tamanho_celula) for i in range(self.num_segmentos)]

            self.angulo = 0.0
            self.vel_angular = 0.0

            # Parâmetros das perturbações
            self.forca_perturbacao = 0.02
            self.intervalo_perturbacao = 30
            self.tempo_perturbacao = 0
            self.direcao_perturbacao = 0

            # Cores
            self.verde_escuro = (0, 100, 0)
            self.verde = (0, 200, 0)
            self.vermelho = (200, 0, 0)

        def aplicar_rotacao(self, ponto, angulo):
            cos_a = math.cos(angulo)
            sin_a = math.sin(angulo)
            x, y = ponto
            return (x * cos_a - y * sin_a, x * sin_a + y * cos_a)

        def atualizar_equilibrio(self, teclas):
            # Torque do jogador
            if teclas[pygame.K_a]:
                self.vel_angular -= 0.005
            if teclas[pygame.K_d]:
                self.vel_angular += 0.005

            # Perturbação externa
            self.tempo_perturbacao += 1
            if self.tempo_perturbacao >= self.intervalo_perturbacao:
                self.tempo_perturbacao = 0
                self.direcao_perturbacao = random.choice([-1, -1, 0, 1, 1])
                self.vel_angular += self.direcao_perturbacao * self.forca_perturbacao

            # Amortecimento
            self.vel_angular *= 0.98
            self.angulo += self.vel_angular

            # Verifica se perdeu
            return abs(self.angulo) <= 0.9  # True se ainda está equilibrando

        def desenhar(self, tela):
            # Desenha os segmentos
            for i, rel in enumerate(self.rel_pos):
                rot = self.aplicar_rotacao(rel, self.angulo)
                x = self.pivo[0] + rot[0]
                y = self.pivo[1] + rot[1]
                cor = self.verde_escuro if i == self.num_segmentos - 1 else self.verde
                pygame.draw.rect(tela, cor,
                                 (x - self.tamanho_celula // 2,
                                  y - self.tamanho_celula // 2,
                                  self.tamanho_celula,
                                  self.tamanho_celula))
                if i != self.num_segmentos - 1:
                    pygame.draw.rect(tela, cor,
                                     (x - self.tamanho_celula // 2,
                                      y - self.tamanho_celula // 2,
                                      self.tamanho_celula,
                                      self.tamanho_celula), 2)

            # Seta indicando direção da perturbação
            if self.direcao_perturbacao != 0:
                centro = (self.pivo[0], self.pivo[1] + 30)
                fim = (centro[0] + self.direcao_perturbacao * 40, centro[1])
                pygame.draw.line(tela, self.vermelho, centro, fim, 4)
                if self.direcao_perturbacao > 0:
                    pygame.draw.polygon(tela, self.vermelho,
                                        [(fim[0], fim[1]),
                                         (fim[0] - 10, fim[1] - 5),
                                         (fim[0] - 10, fim[1] + 5)])
                elif self.direcao_perturbacao < 0:
                    pygame.draw.polygon(tela, self.vermelho,
                                        [(fim[0], fim[1]),
                                         (fim[0] + 10, fim[1] - 5),
                                         (fim[0] + 10, fim[1] + 5)])

    # Instancia a cobra
    cobra = CobraEquilibrio(num_segmentos)

    # Temporizador de 10 segundos
    tempo_restante = 10.0
    rodando = True

    while rodando:
        dt = clock.tick(60) / 1000  # delta em segundos
        tempo_restante -= dt

        # Processa eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 0

        # Captura teclas
        teclas = pygame.key.get_pressed()

        # Atualiza estado do jogo
        if not cobra.atualizar_equilibrio(teclas):
            # Perdeu (caiu)
            break

        # Se tempo acabou, venceu
        if tempo_restante <= 0:
            break

        # Desenha tudo
        TELA.fill((255, 255, 255))
        cobra.desenhar(TELA)

        # Mostra o tempo na tela
        fonte = pygame.font.Font(None, 30)
        texto_tempo = fonte.render(f"{tempo_restante:.1f}s", True, (0, 0, 0))
        TELA.blit(texto_tempo, (10, 10))

        pygame.display.flip()

    # Fim do jogo
    pygame.quit()

    if tempo_restante <= 0:
        # Sobreviveu: retorna ganho aleatório entre 100 e 200
        return random.randint(100, 200)
    else:
        # Morreu: retorna 0
        return 0


# ======================
# Bloco de teste (opcional, para executar diretamente)
# ======================
if __name__ == "__main__":
    # Exemplo: testa com 300 calorias (3 segmentos)
    resultado = minigame_equilibrio(600)
    print(f"Resultado do jogo: {resultado}")