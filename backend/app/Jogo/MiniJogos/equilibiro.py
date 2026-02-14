import pygame
import sys
import math
import random

# Inicialização
pygame.init()
LARGURA, ALTURA = 600, 400
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Equilíbrio na Cobra")
clock = pygame.time.Clock()

# Cores
VERDE_ESCURO = (0, 100, 0)
VERDE = (0, 200, 0)
VERMELHO = (200, 0, 0)

class CobraEquilibrio:
    def __init__(self):
        self.tamanho_celula = 20
        self.num_segmentos = 6         # "seis de altura"
        self.pivo = (LARGURA // 2, ALTURA - 100)  # base da cobra

        # Posições relativas ao pivô (crescem para cima, y negativo)
        self.rel_pos = [(0, -i * self.tamanho_celula) for i in range(self.num_segmentos)]

        self.angulo = 0.0          # radianos
        self.vel_angular = 0.0

        # Parâmetros das perturbações
        self.forca_perturbacao = 0.02      # intensidade do impulso
        self.intervalo_perturbacao = 30    # frames entre impulsos
        self.tempo_perturbacao = 0
        self.direcao_perturbacao = 0       # -1 (esquerda), 0, 1 (direita)

    def aplicar_rotacao(self, ponto, angulo):
        """Rotaciona um ponto (x,y) em torno da origem."""
        cos_a = math.cos(angulo)
        sin_a = math.sin(angulo)
        x, y = ponto
        return (x * cos_a - y * sin_a, x * sin_a + y * cos_a)

    def atualizar_equilibrio(self, teclas):
        # Torque do jogador
        if teclas[pygame.K_a]:
            self.vel_angular -= 0.005   # inclina para esquerda
        if teclas[pygame.K_d]:
            self.vel_angular += 0.005   # inclina para direita

        # Perturbação externa (força para desequilibrar)
        self.tempo_perturbacao += 1
        if self.tempo_perturbacao >= self.intervalo_perturbacao:
            self.tempo_perturbacao = 0
            # Escolhe direção: -1, 0 ou 1 (com viés para não ser sempre agressivo)
            self.direcao_perturbacao = random.choice([-1, -1, 0, 1, 1])
            # Aplica impulso na velocidade angular
            self.vel_angular += self.direcao_perturbacao * self.forca_perturbacao

        # Amortecimento natural
        self.vel_angular *= 0.98

        # Atualiza ângulo
        self.angulo += self.vel_angular

        # Verifica se perdeu (ângulo muito grande)
        if abs(self.angulo) > 0.9:  # ~51 graus
            return False
        return True

    def desenhar(self):
        # Desenha os segmentos rotacionados
        for i, rel in enumerate(self.rel_pos):
            rot = self.aplicar_rotacao(rel, self.angulo)
            x = self.pivo[0] + rot[0]
            y = self.pivo[1] + rot[1]
            cor = VERDE_ESCURO if i == self.num_segmentos - 1 else VERDE
            pygame.draw.rect(TELA, cor,
                             (x - self.tamanho_celula//2,
                              y - self.tamanho_celula//2,
                              self.tamanho_celula,
                              self.tamanho_celula))
            if i != self.num_segmentos - 1:
                pygame.draw.rect(TELA, cor,
                                 (x - self.tamanho_celula//2,
                                  y - self.tamanho_celula//2,
                                  self.tamanho_celula,
                                  self.tamanho_celula), 2)

        # Opcional: desenha indicador da força (seta)
        if self.direcao_perturbacao != 0:
            centro = (self.pivo[0], self.pivo[1] + 30)  # em baixo da cobra
            fim = (centro[0] + self.direcao_perturbacao * 40, centro[1])
            pygame.draw.line(TELA, VERMELHO, centro, fim, 4)
            # ponta da seta
            if self.direcao_perturbacao > 0:
                pygame.draw.polygon(TELA, VERMELHO,
                                    [(fim[0], fim[1]),
                                     (fim[0]-10, fim[1]-5),
                                     (fim[0]-10, fim[1]+5)])
            elif self.direcao_perturbacao < 0:
                pygame.draw.polygon(TELA, VERMELHO,
                                    [(fim[0], fim[1]),
                                     (fim[0]+10, fim[1]-5),
                                     (fim[0]+10, fim[1]+5)])

    def reiniciar(self):
        self.angulo = 0.0
        self.vel_angular = 0.0
        self.tempo_perturbacao = 0
        self.direcao_perturbacao = 0

# Loop principal
cobra = CobraEquilibrio()
rodando = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and not rodando:
                cobra.reiniciar()
                rodando = True

    if rodando:
        teclas = pygame.key.get_pressed()
        rodando = cobra.atualizar_equilibrio(teclas)

    TELA.fill((255, 255, 255))
    cobra.desenhar()

    if not rodando: # desenhar mais encima do que a cobra
        fonte = pygame.font.Font(None, 36)
        texto = fonte.render("Game Over - Pressione R para reiniciar", True, (0, 0, 0))
        TELA.blit(texto, (LARGURA//2 - texto.get_width()//2, ALTURA//2 - 50))

    pygame.display.flip()
    clock.tick(60)